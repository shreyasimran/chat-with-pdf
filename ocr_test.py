import fitz
import pytesseract
from PIL import Image

pytesseract.pytesseract.tesseract_cmd = (
    r"C:\Program Files\Tesseract-OCR\tesseract.exe"
)

pdf_path = r"data\pdfs\CO - Unit 1.pdf"

doc = fitz.open(pdf_path)

page = doc[0]

pix = page.get_pixmap()

image = Image.frombytes(
    "RGB",
    [pix.width, pix.height],
    pix.samples
)

text = pytesseract.image_to_string(image)

print("----- OCR TEXT -----")
print(text)

doc.close()