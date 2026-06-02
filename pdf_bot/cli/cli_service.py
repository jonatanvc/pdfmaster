import fitz  # PyMuPDF
from gettext import gettext as _
from pathlib import Path

from loguru import logger

from pdf_bot.cli.exceptions import CLINonZeroExitStatusError


class CLIService:
    def compress_pdf(self, input_path: Path, output_path: Path) -> None:
        try:
            doc = fitz.open(input_path)
            # garbage=4: Remove unreferenced objects, compress streams, etc.
            # deflate=True: Compress streams
            doc.save(output_path, garbage=4, deflate=True)
            doc.close()
        except Exception as e:
            logger.error(f"Failed to compress PDF with PyMuPDF: {e}")
            raise CLINonZeroExitStatusError(_("Failed to complete process"))

    def extract_pdf_images(self, input_path: Path, output_path: Path) -> None:
        try:
            doc = fitz.open(input_path)
            # Create the images directory since pdfimages would normally create it or output files with that prefix
            # Wait, the original command was `pdfimages -png input output_path/images`
            # so it creates files like `output_path/images-000.png`
            prefix = str(output_path / "images")
            img_count = 0
            for page in doc:
                images = page.get_images(full=True)
                for img in images:
                    xref = img[0]
                    pix = fitz.Pixmap(doc, xref)
                    if pix.n - pix.alpha > 3:  # CMYK or non-RGB
                        pix = fitz.Pixmap(fitz.csRGB, pix)
                    
                    pix.save(f"{prefix}-{img_count:03d}.png")
                    pix = None
                    img_count += 1
            doc.close()
        except Exception as e:
            logger.error(f"Failed to extract images with PyMuPDF: {e}")
            raise CLINonZeroExitStatusError(_("Failed to complete process"))

