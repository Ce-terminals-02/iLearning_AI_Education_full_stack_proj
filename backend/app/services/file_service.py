import io
from PyPDF2 import PdfReader

def extract_text(filename: str, content: bytes) -> str:
    if filename.lower().endswith('.pdf'):
        reader = PdfReader(io.BytesIO(content))
        text = "\n".join(page.extract_text() or '' for page in reader.pages)
        return text
    elif filename.lower().endswith('.txt'):
        return content.decode('utf-8')
    else:
        raise ValueError('Unsupported file type. Only PDF and TXT are supported.') 