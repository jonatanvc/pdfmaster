from typing import Any

import sentry_sdk
from dependency_injector.providers import Singleton
from dependency_injector.wiring import Provide, inject
from loguru import logger
from telegram.ext import Application as TelegramApp

from pdf_bot.containers import Application
from pdf_bot.database import DatabaseClient
from pdf_bot.error import ErrorHandler
from pdf_bot.log import MyLogHandler
from pdf_bot.settings import Settings
from pdf_bot.telegram_handler import AbstractTelegramHandler


@inject
def main(
    telegram_app: TelegramApp,
    settings: Settings | dict[str, Any] = Provide[Application.core.settings],
    log_handler: MyLogHandler = Provide[Application.core.log_handler],
    db_client: DatabaseClient = Provide[Application.clients.database],
) -> None:
    log_handler.setup()

    # There's a bug where configurations are passed as a dict, so we attempt to pass it
    # here. See https://github.com/ets-labs/python-dependency-injector/issues/593
    if isinstance(settings, dict):
        settings = Settings(**settings)

    # Initialize PostgreSQL database tables
    if db_client.check_connection():
        db_client.create_tables()
        logger.info("PostgreSQL database initialized successfully")
    else:
        logger.error("Failed to connect to PostgreSQL database")

    if settings.sentry_dsn is not None:
        sentry_sdk.init(settings.sentry_dsn, traces_sample_rate=0.8, profiles_sample_rate=0.8)
    else:
        logger.warning("SENTRY_DSN not set")

    async def post_init(app: TelegramApp) -> None:
        from pdf_bot.tasks.cleanup import cleanup_temp_files_loop
        import asyncio
        asyncio.create_task(cleanup_temp_files_loop())

    telegram_app.post_init = post_init
    
    settings_obj = app.core.settings()
    if settings_obj.get("webhook_url"):
        logger.info(f"Starting webhook on port {settings_obj.get('port', 8080)}...")
        telegram_app.run_webhook(
            listen="0.0.0.0",
            port=settings_obj.get("port", 8080),
            webhook_url=settings_obj["webhook_url"]
        )
    else:
        logger.info("Starting polling...")
        telegram_app.run_polling()


if __name__ == "__main__":
    import sys

    logger.info("Starting PDF Bot...")

    try:
        app = Application()
    except Exception:
        logger.exception("Failed to create Application container")
        sys.exit(1)

    app.wire(modules=[__name__])

    builder = TelegramApp.builder().bot(app.core.telegram_bot()).concurrent_updates(True)
    
    settings_obj = app.core.settings()
    if settings_obj.get("redis_url"):
        try:
            from telegram.ext import RedisPersistence
            from redis.asyncio import Redis
            
            redis_client = Redis.from_url(settings_obj["redis_url"])
            persistence = RedisPersistence(redis_client)
            builder = builder.persistence(persistence)
            logger.info("RedisPersistence enabled for Telegram bot state.")
        except ImportError:
            logger.warning("Redis dependencies not installed. Falling back to memory persistence.")
            
    _telegram_app = builder.build()

    # Dependency injectior only initialises the classes if they are referenced. Since
    # the processors are not referenced anywhere, we need to explicitly initialise them
    # so that they're registered under AbstractFileProcessor
    for provider in app.processors.providers.values():  # type: ignore[attr-defined]
        if isinstance(provider, Singleton):
            provider()

    # Similarly, initialise and register all the handlers for the bot
    for provider in app.handlers.providers.values():  # type: ignore[attr-defined]
        if isinstance(provider, Singleton):
            handler = provider()
            if isinstance(handler, AbstractTelegramHandler):
                _telegram_app.add_handlers(handler.handlers)
            elif isinstance(handler, ErrorHandler):
                _telegram_app.add_error_handler(handler.callback)

    main(_telegram_app)
