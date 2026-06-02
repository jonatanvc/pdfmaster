from dependency_injector import containers, providers
from requests import Session
from telegram.ext import AIORateLimiter, ExtBot
from telegram.request import HTTPXRequest
from pdf_bot.account import AccountRepository, AccountService
from pdf_bot.analytics import AnalyticsRepository, AnalyticsService
from pdf_bot.cli import CLIService
from pdf_bot.command import CommandService, MyCommandHandler
from pdf_bot.compare import CompareHandler, CompareService
from pdf_bot.database import DatabaseClient
from pdf_bot.document import DocumentService
from pdf_bot.document_processor import DocumentTaskProcessor, DocumentToPdfProcessor
from pdf_bot.error import ErrorCallbackQueryHandler, ErrorHandler, ErrorService
from pdf_bot.file import FileHandler, FileService
from pdf_bot.image import ImageService
from pdf_bot.image_handler import BatchImageHandler, BatchImageService
from pdf_bot.image_processor import BeautifyImageProcessor, ImageTaskProcessor, ImageToPdfProcessor
from pdf_bot.io_internal import IOService
from pdf_bot.language import LanguageHandler, LanguageRepository, LanguageService
from pdf_bot.log import InterceptLoggingHandler, MyLogHandler
from pdf_bot.merge import MergeHandler, MergeService
from pdf_bot.pdf import PdfService
from pdf_bot.pdf_processor import (
    CompressPdfProcessor,
    CropPdfProcessor,
    DecryptPdfProcessor,
    EncryptPdfProcessor,
    ExtractPdfImageProcessor,
    ExtractPdfTextProcessor,
    GrayscalePdfProcessor,
    OcrPdfProcessor,
    PdfTaskProcessor,
    PdfToImageProcessor,
    PreviewPdfProcessor,
    RenamePdfProcessor,
    RotatePdfProcessor,
    ScalePdfProcessor,
    SplitPdfProcessor,
)
from pdf_bot.settings import Settings
from pdf_bot.stats import StatsService
from pdf_bot.telegram_internal import TelegramService
from pdf_bot.text import TextHandler, TextRepository, TextService
from pdf_bot.watermark import WatermarkHandler, WatermarkService
from pdf_bot.webpage import WebpageHandler, WebpageService

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

