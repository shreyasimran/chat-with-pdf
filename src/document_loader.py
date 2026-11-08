from pypdf import PdfReader
import fitz
import pytesseract
from PIL import Image
import os

if os.name == "nt":
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )




def load_pdf(pdf_path):

    reader = PdfReader(pdf_path)
    doc = fitz.open(pdf_path)

    pages = []

    for page_number, page in enumerate(reader.pages, start=1):

        text = page.extract_text() or ""

        # If PDF has no usable text, use OCR
        if len(text.strip()) < 20:

            pdf_page = doc[page_number - 1]

            pix = pdf_page.get_pixmap()

            image = Image.frombytes(
                "RGB",
                [pix.width, pix.height],
                pix.samples
            )

            text = pytesseract.image_to_string(image)

        pages.append({
            "text": text,
            "page_number": page_number
        })

    doc.close()

    return pages