from pydantic import BaseModel
from typing import List

class UserCreate(BaseModel):
    username: str
    password: str

class User(BaseModel):
    id: int
    username: str

    class Config:
        orm_mode = True

class Test(BaseModel):
    id: int
    title: str
    description: str

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: str = None
    
    # Модель для создания вопроса
class QuestionCreate(BaseModel):
    text: str
    options: List[str]
    correct_answer: str
    test_id: int

# Модель для представления вопроса
class Question(BaseModel):
    id: int
    text: str
    test_id: int
    options: List[str]
    correct_answer: str

    class Config:
        orm_mode = True

# Модель для ответов на тест
class TestAnswers(BaseModel):
    answers: Dict[str, str]  # {question_id: answer}

# Модель для результата теста
class TestResult(BaseModel):
    correct_answers: int
    total_questions: int