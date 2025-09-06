from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime

class Feedback(BaseModel):
    id: int
    name: str
    email: EmailStr
    course: str
    rating: int
    tags: List[str] = []
    comments: str
    submitted_at: datetime

class FeedbackCreate(BaseModel):
    name: str
    email: EmailStr
    course: str
    rating: int
    tags: Optional[List[str]] = []
    comments: str
