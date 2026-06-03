from dependency_injector import containers, providers
from telegram.ext import AIORateLimiter, ExtBot
from telegram.request import HTTPXRequest
from pdf_bot.log import InterceptLoggingHandler, MyLogHandler
from pdf_bot.settings import Settings


class Core(containers.DeclarativeContainer):
    settings = providers.Configuration(pydantic_settings=[Settings()])

    _bot_request = providers.Singleton(
        HTTPXRequest,
        connection_pool_size=settings.request_connection_pool_size,
        read_timeout=settings.request_read_timeout,
        write_timeout=settings.request_write_timeout,
        connect_timeout=settings.request_connect_timeout,
        pool_timeout=settings.request_pool_timeout,
    )
    _bot_rate_limiter = providers.Singleton(
        AIORateLimiter, max_retries=settings.telegram_max_retries
    )

    telegram_bot = providers.Singleton(
        ExtBot,
        token=settings.telegram_token,
        arbitrary_callback_data=True,
        request=_bot_request,
        rate_limiter=_bot_rate_limiter,
    )

    intercept_logging_handler = providers.Singleton(InterceptLoggingHandler)
    log_handler = providers.Singleton(
        MyLogHandler, intercept_logging_handler=intercept_logging_handler
    )

