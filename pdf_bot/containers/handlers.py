from dependency_injector import containers, providers
from pdf_bot.command import MyCommandHandler
from pdf_bot.compare import CompareHandler
from pdf_bot.error import ErrorCallbackQueryHandler, ErrorHandler
from pdf_bot.file import FileHandler
from pdf_bot.image_handler import BatchImageHandler
from pdf_bot.language import LanguageHandler
from pdf_bot.merge import MergeHandler
from pdf_bot.settings import Settings
from pdf_bot.text import TextHandler
from pdf_bot.watermark import WatermarkHandler
from pdf_bot.webpage import WebpageHandler

class Handlers(containers.DeclarativeContainer):
    _settings = providers.Configuration(pydantic_settings=[Settings()])
    services = providers.DependenciesContainer()

    error = providers.Singleton(ErrorHandler, language_service=services.language)

    command = providers.Singleton(
        MyCommandHandler,
        command_service=services.command,
        stats_service=services.stats,
        admin_telegram_id=_settings.admin_telegram_id,
    )
    language = providers.Singleton(LanguageHandler, language_service=services.language)

    # Make sure webpage handler comes before the file processors to capture the URLs
    webpage = providers.Singleton(WebpageHandler, webpage_service=services.webpage)

    compare = providers.Singleton(
        CompareHandler,
        compare_service=services.compare,
        telegram_service=services.telegram,
    )
    image = providers.Singleton(
        BatchImageHandler,
        batch_image_service=services.batch_image,
        telegram_service=services.telegram,
    )
    merge = providers.Singleton(
        MergeHandler, merge_service=services.merge, telegram_service=services.telegram
    )
    text = providers.Singleton(
        TextHandler, text_service=services.text, telegram_service=services.telegram
    )
    watermark = providers.Singleton(
        WatermarkHandler,
        watermark_service=services.watermark,
        telegram_service=services.telegram,
    )

    # Make sure the file handler comes after the other file related file handlers
    # so that it doesn't take over when those handlers are expecting a file
    file = providers.Singleton(
        FileHandler, file_service=services.file, telegram_service=services.telegram
    )

    # This is the catch all callback query handler so make sure it comes last
    error_callback_query = providers.Singleton(
        ErrorCallbackQueryHandler, error_service=services.error
    )

