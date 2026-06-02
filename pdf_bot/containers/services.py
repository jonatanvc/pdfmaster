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

class Services(containers.DeclarativeContainer):
    _settings = providers.Configuration(pydantic_settings=[Settings()])
    core = providers.DependenciesContainer()
    clients = providers.DependenciesContainer()
    repositories = providers.DependenciesContainer()

    cli = providers.Singleton(CLIService)
    io = providers.Singleton(IOService)

    language = providers.Singleton(LanguageService, language_repository=repositories.language)

    account = providers.Singleton(
        AccountService,
        account_repository=repositories.account,
        language_service=language,
    )
    analytics = providers.Singleton(
        AnalyticsService,
        analytics_repository=repositories.analytics,
        language_service=language,
    )
    command = providers.Singleton(
        CommandService, account_service=account, language_service=language
    )
    stats = providers.Singleton(StatsService, db_client=clients.database)
    error = providers.Singleton(ErrorService, language_service=language)
    telegram = providers.Singleton(
        TelegramService,
        io_service=io,
        language_service=language,
        analytics_service=analytics,
        bot=core.telegram_bot,
    )

    image = providers.Singleton(
        ImageService, cli_service=cli, io_service=io, telegram_service=telegram
    )
    pdf = providers.Singleton(PdfService, cli_service=cli, io_service=io, telegram_service=telegram)
    document = providers.Singleton(
        DocumentService, io_service=io, telegram_service=telegram
    )

    _image_task = providers.Singleton(ImageTaskProcessor, language_service=language)
    _pdf_task = providers.Singleton(PdfTaskProcessor, language_service=language)
    _document_task = providers.Singleton(DocumentTaskProcessor, language_service=language)
    file = providers.Singleton(
        FileService,
        telegram_service=telegram,
        language_service=language,
        image_task_processor=_image_task,
        pdf_task_processor=_pdf_task,
        document_task_processor=_document_task,
    )

    compare = providers.Singleton(
        CompareService,
        pdf_service=pdf,
        telegram_service=telegram,
        language_service=language,
    )
    batch_image = providers.Singleton(
        BatchImageService,
        image_service=image,
        telegram_service=telegram,
        language_service=language,
    )

    merge = providers.Singleton(
        MergeService,
        pdf_service=pdf,
        telegram_service=telegram,
        language_service=language,
    )
    text = providers.Singleton(
        TextService,
        text_repository=repositories.text,
        pdf_service=pdf,
        telegram_service=telegram,
        language_service=language,
    )
    watermark = providers.Singleton(
        WatermarkService,
        pdf_service=pdf,
        telegram_service=telegram,
        language_service=language,
    )
    webpage = providers.Singleton(
        WebpageService,
        io_service=io,
        telegram_service=telegram,
        language_service=language,
    )

