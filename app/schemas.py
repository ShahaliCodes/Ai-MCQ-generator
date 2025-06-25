from typing import List
from pydantic import BaseModel

class QuestionOption(BaseModel):
    id: int
    text: str
    is_correct: bool

class Question(BaseModel):
    id: int
    text: str
    options: List[QuestionOption]
    explanation: str

class QuestionSet(BaseModel):
    file_url: str
    original_filename: str
    questions: List[Question]