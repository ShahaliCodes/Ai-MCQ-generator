from pydantic import BaseModel
from typing import List

class Question(BaseModel):
    question: str
    options: List[str]
    answer: str

class QuestionSet(BaseModel):
    file_url: str
    original_filename: str
    questions: List[Question]