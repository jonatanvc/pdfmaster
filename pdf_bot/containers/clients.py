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

class Clients(containers.DeclarativeContainer):
    _settings = providers.Configuration(pydantic_settings=[Settings()])

    _session = Session()
    _session.hooks = {  # noqa: RUF012
        "response": lambda r, *_args, **_kwargs: r.raise_for_status()  # pragma: no cover
    }

    api = providers.Object(_session)
    database = providers.Singleton(DatabaseClient, database_url=_settings.database_url)

