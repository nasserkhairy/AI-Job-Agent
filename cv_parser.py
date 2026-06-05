import re
from pypdf import PdfReader


def clean_text(text):

    text = re.sub(r'(?<=\w)\s(?=\w)', '', text)

    text = re.sub(r'\s+', ' ', text)

    return text


def extract_cv_text(file_path):

    reader = PdfReader(file_path)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return clean_text(text)