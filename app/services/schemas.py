from typing import List, Optional
from pydantic import BaseModel, Field
from enum import Enum

class FileType(str, Enum):
    PDF = "pdf"
    DOCX = "docx"
    XLSX = "xlsx"
    JPG = "jpg"
    PNG = "png"
    TXT = "txt"
    PPTX = "pptx"

class QuestionOption(BaseModel):
    id: str = Field(..., example="A")
    text: str = Field(..., example="Paris")
    is_correct: bool = Field(..., example=True)

class Question(BaseModel):
    id: int = Field(..., example=1)
    text: str = Field(..., example="What is the capital of France?")
    options: List[QuestionOption]
    explanation: str = Field(..., example="Paris has been the capital of France since 508 AD")

class QuestionSet(BaseModel):
    file_url: str = Field(..., example="https://example.com/file.pdf")
    original_filename: str = Field(..., example="document.pdf")
    questions: List[Question]

class ErrorResponse(BaseModel):
    detail: str = Field(..., example="Error message")

class HealthCheck(BaseModel):
    status: str = Field(..., example="healthy")