from pydantic import BaseModel
from typing import List


class MCQ(BaseModel):
    question: str
    options: List[str]
    answer: str


class StudyMaterialResponse(BaseModel):
    message: str
    filename: str
    transcript: str
    summary: str
    key_points: List[str]
    mcqs: List[MCQ]
    viva: List[str]
    pdf: str