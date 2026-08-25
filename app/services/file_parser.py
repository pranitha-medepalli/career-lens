from fastapi import UploadFile
from pypdf import PdfReader
from docx import Document
import io


async def extract_text_from_file(file: UploadFile) -> str:

    content = await file.read()

    filename = file.filename.lower()

    if filename.endswith(".pdf"):
        return extract_pdf_text(content)

    elif filename.endswith(".docx"):
        return extract_docx_text(content)

    else:
        raise ValueError(
            "Unsupported file format. Please upload PDF or DOCX."
        )


def extract_pdf_text(content: bytes) -> str:

    pdf_file = io.BytesIO(content)

    reader = PdfReader(pdf_file)

    text = ""

    for page in reader.pages:

        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx_text(content: bytes) -> str:

    docx_file = io.BytesIO(content)

    document = Document(docx_file)

    text = ""

    for paragraph in document.paragraphs:

        if paragraph.text.strip():
            text += paragraph.text + "\n"

    return text