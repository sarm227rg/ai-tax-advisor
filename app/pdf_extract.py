# NOTE: PyPDF2 must be installed for this import to work.
import PyPDF2


def extract_pdf_data(pdf_path):
    """
    Extracts data from a PDF file using PyPDF2 for text only.
    Returns a dictionary with all UserFinancials fields as keys.
    OCR is skipped (no pdf2image, no pytesseract, no Poppler required).
    """
    with open(pdf_path, 'rb') as f:
        reader = PyPDF2.PdfReader(f)
        text = "\n".join(page.extract_text() or '' for page in reader.pages)
    # For now, return all fields as empty strings (or dummy values), plus raw_text
    return {
        'gross_salary': '',
        'basic_salary': '',
        'hra_received': '',
        'rent_paid': '',
        'deduction_80c': '',
        'deduction_80d': '',
        'standard_deduction': '',
        'professional_tax': '',
        'tds': '',
        'raw_text': text
    } 