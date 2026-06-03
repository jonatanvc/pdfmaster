from dependency_injector import containers, providers
from pdf_bot.document_processor import DocumentToPdfProcessor
from pdf_bot.image_processor import BeautifyImageProcessor, ImageToPdfProcessor
from pdf_bot.pdf_processor import CompressPdfProcessor, CropPdfProcessor, DecryptPdfProcessor, EncryptPdfProcessor, ExtractPdfImageProcessor, ExtractPdfTextProcessor, GrayscalePdfProcessor, OcrPdfProcessor, PdfToImageProcessor, PreviewPdfProcessor, RenamePdfProcessor, RotatePdfProcessor, ScalePdfProcessor, SplitPdfProcessor

class Processors(containers.DeclarativeContainer):
    services = providers.DependenciesContainer()

    compress = providers.Singleton(
        CompressPdfProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    crop = providers.Singleton(
        CropPdfProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    decrypt = providers.Singleton(
        DecryptPdfProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    encrypt = providers.Singleton(
        EncryptPdfProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    extract_image = providers.Singleton(
        ExtractPdfImageProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    extract_text = providers.Singleton(
        ExtractPdfTextProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    grayscale = providers.Singleton(
        GrayscalePdfProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    ocr = providers.Singleton(
        OcrPdfProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    pdf_to_image = providers.Singleton(
        PdfToImageProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    preview_pdf = providers.Singleton(
        PreviewPdfProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    rename = providers.Singleton(
        RenamePdfProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    rotate = providers.Singleton(
        RotatePdfProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    scale = providers.Singleton(
        ScalePdfProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    split = providers.Singleton(
        SplitPdfProcessor,
        pdf_service=services.pdf,
        telegram_service=services.telegram,
        language_service=services.language,
    )

    beautify = providers.Singleton(
        BeautifyImageProcessor,
        image_service=services.image,
        telegram_service=services.telegram,
        language_service=services.language,
    )
    image_to_pdf = providers.Singleton(
        ImageToPdfProcessor,
        image_service=services.image,
        telegram_service=services.telegram,
        language_service=services.language,
    )

    document_to_pdf = providers.Singleton(
        DocumentToPdfProcessor,
        document_service=services.document,
        telegram_service=services.telegram,
        language_service=services.language,
    )

