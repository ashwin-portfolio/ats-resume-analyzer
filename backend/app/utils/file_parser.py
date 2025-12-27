"""
File parsing utilities for extracting text from PDF and DOCX files.
Includes file content validation using magic bytes.
"""
import io
from typing import Optional, Tuple
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


# Magic bytes (file signatures) for validation
PDF_MAGIC_BYTES = [b"%PDF"]
DOCX_MAGIC_BYTES = [
    b"PK\x03\x04",  # ZIP signature (DOCX is a ZIP file)
    b"PK\x05\x06",  # Empty ZIP
    b"PK\x07\x08",  # Spanned ZIP
]
DOC_MAGIC_BYTES = [
    b"\xd0\xcf\x11\xe0\xa1\xb1\x1a\xe1",  # OLE2 signature (old .doc format)
]


def validate_file_content(file_content: bytes, file_extension: str) -> Tuple[bool, str]:
    """
    Validate file content by checking magic bytes (file signatures).
    This prevents file type spoofing attacks.
    
    Args:
        file_content: File content as bytes
        file_extension: Expected file extension (e.g., '.pdf', '.docx')
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    if len(file_content) < 8:
        return False, "File is too small to be valid"
    
    file_extension = file_extension.lower()
    file_start = file_content[:8]
    
    if file_extension == '.pdf':
        # Check for PDF magic bytes
        if not any(file_content.startswith(magic) for magic in PDF_MAGIC_BYTES):
            return False, "File does not appear to be a valid PDF (invalid file signature)"
    
    elif file_extension == '.docx':
        # DOCX files are ZIP archives, check for ZIP signature
        if not any(file_content.startswith(magic) for magic in DOCX_MAGIC_BYTES):
            return False, "File does not appear to be a valid DOCX (invalid file signature)"
        # Additional check: DOCX should contain specific files in ZIP
        # This is a basic check; more thorough validation would unzip and check structure
    
    elif file_extension == '.doc':
        # Old DOC format uses OLE2
        if not any(file_content.startswith(magic) for magic in DOC_MAGIC_BYTES):
            return False, "File does not appear to be a valid DOC (invalid file signature)"
    
    return True, ""


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
        raise ValueError(f"Failed to extract text from PDF: {str(e)}")


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
        raise ValueError(f"Failed to extract text from DOCX: {str(e)}")


def extract_text_from_file(file_content: bytes, file_extension: str, validate_content: bool = True) -> str:
    """
    Extract text from file based on extension.
    Optionally validates file content using magic bytes.
    
    Args:
        file_content: File content as bytes
        file_extension: File extension (e.g., '.pdf', '.docx')
        validate_content: Whether to validate file content using magic bytes (default: True)
        
    Returns:
        Extracted text string
        
    Raises:
        ValueError: If file type is not supported, validation fails, or parsing fails
    """
    file_extension = file_extension.lower()
    
    # Validate file content if requested
    if validate_content:
        is_valid, error_msg = validate_file_content(file_content, file_extension)
        if not is_valid:
            logger.warning(f"File content validation failed: {error_msg}")
            raise ValueError(f"Invalid file content: {error_msg}")
    
    if file_extension == '.pdf':
        return extract_text_from_pdf(file_content)
    elif file_extension == '.docx':
        return extract_text_from_docx(file_content)
    elif file_extension == '.doc':
        # Old .doc format (OLE2) - python-docx doesn't support it
        # Note: Old .doc files require additional libraries like python-docx2txt or antiword
        # For now, we'll raise an error with a helpful message
        raise ValueError(
            "Old .doc format (OLE2) is not supported. "
            "Please convert your file to .docx or .pdf format. "
            "You can use Microsoft Word or online converters to convert .doc to .docx"
        )
    else:
        raise ValueError(f"Unsupported file type: {file_extension}. Supported: .pdf, .docx")


