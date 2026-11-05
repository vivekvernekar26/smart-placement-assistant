"""
Pydantic schemas for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class QuestionBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    category: str = Field(..., min_length=1, max_length=60)
    difficulty: str = Field(default="Beginner", max_length=20)
    description: str = Field(..., min_length=1)
    sample_input: Optional[str] = None
    expected_output: Optional[str] = None

class QuestionCreate(QuestionBase):
    pass

class QuestionResponse(QuestionBase):
    question_id: int
    
    class Config:
        from_attributes = True

class AttemptCreate(BaseModel):
    student_id: int = Field(..., gt=0)
    question_id: int = Field(..., gt=0)
    submitted_answer: Optional[str] = None
    score: float = Field(default=0, ge=0, le=100)
    completed: bool = Field(default=False)

class AttemptResponse(BaseModel):
    attempt_id: int
    student_id: int
    question_id: int
    submitted_answer: Optional[str]
    score: float
    completed: bool
    attempted_at: datetime
    
    class Config:
        from_attributes = True

class ProgressResponse(BaseModel):
    student_id: int
    total_attempts: int
    completed_questions: int
    average_score: float
    attempts: list

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=500)

class ChatResponse(BaseModel):
    message: str
    response: str
