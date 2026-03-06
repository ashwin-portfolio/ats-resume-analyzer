"""
File parsing utilities for extracting text from PDF and DOCX files.
"""
import io
import logging

try:
    from PyPDF2 import PdfReader
except ImportError:
    PdfReader = None

try:
    from docx import Document
except ImportError:
    Document = None

logger = logging.getLogger(__name__)


def extract_text_from_pdf(file_content: bytes) -> str:
    """
    Extract text from PDF file content.
    
    Args:
        file_content: PDF file as bytes
        
    Returns:
        Extracted text string
        
    Raises:
        ValueError: If PDF parsing fails
    """
    if PdfReader is None:
        raise ImportError("PyPDF2 is not installed. Install it with: pip install PyPDF2")
    
    try:
        pdf_file = io.BytesIO(file_content)
        reader = PdfReader(pdf_file)
        
        text_parts = []
        for page in reader.pages:
            text = page.extract_text()
            if text:
                text_parts.append(text)
        
        full_text = "\n".join(text_parts)
        if not full_text or len(full_text.strip()) < 10:
            raise ValueError("No extractable text found in PDF file")
        logger.info(f"✅ Extracted {len(full_text)} characters from PDF")
        return full_text
        
    except Exception as e:
        logger.error(f"❌ Error extracting text from PDF: {e}")
        raise ValueError(f"Failed to extract text from PDF: {str(e)}") from e


def extract_text_from_docx(file_content: bytes) -> str:
    """
    Extract text from DOCX file content.
    
    Args:
        file_content: DOCX file as bytes
        
    Returns:
        Extracted text string
        
    Raises:
        ValueError: If DOCX parsing fails
    """
    if Document is None:
        raise ImportError("python-docx is not installed. Install it with: pip install python-docx")
    
    try:
        docx_file = io.BytesIO(file_content)
        doc = Document(docx_file)
        
        text_parts = []
        for paragraph in doc.paragraphs:
            if paragraph.text:
                text_parts.append(paragraph.text)
        
        # Also extract text from tables
        for table in doc.tables:
            for row in table.rows:
                for cell in row.cells:
                    if cell.text:
                        text_parts.append(cell.text)
        
        full_text = "\n".join(text_parts)
        if not full_text or len(full_text.strip()) < 10:
            raise ValueError("No extractable text found in DOCX file")
        logger.info(f"✅ Extracted {len(full_text)} characters from DOCX")
        return full_text
        
    except Exception as e:
        logger.error(f"❌ Error extracting text from DOCX: {e}")
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}") from e


def extract_text_from_file(
    file_content: bytes,
    file_extension: str,
    *,
    validate_content: bool = False,
    min_chars: int = 10
) -> str:
    """
    Extract text from file based on extension.
    
    Args:
        file_content: File content as bytes
        file_extension: File extension (e.g., '.pdf', '.docx')
        validate_content: If True, validate extracted text length
        min_chars: Minimum number of non-whitespace characters required when validate_content=True
        
    Returns:
        Extracted text string
        
    Raises:
        ValueError: If file type is not supported or parsing fails
    """
    file_extension = file_extension.lower()
    
    if file_extension == '.pdf':
        text = extract_text_from_pdf(file_content)
    elif file_extension == '.docx':
        text = extract_text_from_docx(file_content)
    elif file_extension == '.doc':
        # `.doc` (legacy Word format) is not supported by python-docx.
        raise ValueError("Legacy .doc files are not supported. Please convert to .docx.")
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Supported: .pdf, .docx")

    if validate_content and (not text or len(text.strip()) < min_chars):
        raise ValueError("No extractable text found in file")

    return text


