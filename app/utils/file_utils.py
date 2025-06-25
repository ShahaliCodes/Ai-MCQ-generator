import os
import mimetypes
from typing import Optional

def get_file_extension(filename: str) -> str:
    """Get file extension from filename"""
    return os.path.splitext(filename)[1].lower().lstrip('.')

def validate_file_type(filename: str, allowed_types: list) -> bool:
    """Validate file type against allowed types"""
    file_ext = get_file_extension(filename)
    return file_ext in allowed_types

def get_mime_type(file_path: str) -> Optional[str]:
    """Get MIME type for a file"""
    mime_type, _ = mimetypes.guess_type(file_path)
    return mime_type

def sanitize_filename(filename: str) -> str:
    """Sanitize filename to remove potentially dangerous characters"""
    keepchars = (' ', '.', '_', '-')
    return "".join(
        c for c in filename if c.isalnum() or c in keepchars
    ).rstrip()