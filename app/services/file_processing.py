import os
import magic
from typing import Union
from io import BytesIO
from pathlib import Path
from PIL import Image
import pandas as pd
from PyPDF2 import PdfReader
from docx import Document
from pptx import Presentation
import xlrd
import logging
from fastapi import HTTPException

logger = logging.getLogger(__name__)

async def process_uploaded_file(file) -> str:
    """Process uploaded file and return extracted text"""
    try:
        content = await file.read()
        file_stream = BytesIO(content)
        
        # Determine file type using python-magic
        file_type = magic.from_buffer(content, mime=True)
        
        if file_type == 'application/pdf':
            return _extract_text_from_pdf(file_stream)
        elif file_type in ['application/vnd.openxmlformats-officedocument.wordprocessingml.document', 'application/msword']:
            return _extract_text_from_docx(file_stream)
        elif file_type in ['application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', 'application/vnd.ms-excel']:
            return _extract_text_from_excel(file_stream)
        elif file_type == 'application/vnd.openxmlformats-officedocument.presentationml.presentation':
            return _extract_text_from_pptx(file_stream)
        elif file_type == 'text/plain':
            return content.decode('utf-8')
        elif file_type in ['image/jpeg', 'image/png']:
            raise HTTPException(
                status_code=400,
                detail="Image text extraction is not supported in this environment"
            )
        else:
            raise HTTPException(
                status_code=400,
                detail=f"Unsupported file type: {file_type}"
            )
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error processing file: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Could not process file: {str(e)}"
        )

def _extract_text_from_pdf(file_stream) -> str:
    reader = PdfReader(file_stream)
    text = ""
    for page in reader.pages:
        text += page.extract_text() or ""
    return text

def _extract_text_from_docx(file_stream) -> str:
    doc = Document(file_stream)
    return "\n".join([para.text for para in doc.paragraphs if para.text])

def _extract_text_from_excel(file_stream) -> str:
    try:
        # Try reading with pandas first
        df = pd.read_excel(file_stream)
        return df.to_string()
    except:
        # Fallback to xlrd for older formats
        workbook = xlrd.open_workbook(file_contents=file_stream.read())
        sheets = [workbook.sheet_by_index(i) for i in range(workbook.nsheets)]
        text = ""
        for sheet in sheets:
            for row in range(sheet.nrows):
                text += "\t".join([str(cell.value) for cell in sheet.row(row)]) + "\n"
        return text

def _extract_text_from_pptx(file_stream) -> str:
    prs = Presentation(file_stream)
    text = []
    for slide in prs.slides:
        for shape in slide.shapes:
            if hasattr(shape, "text"):
                text.append(shape.text)
    return "\n".join(text)
