from sqlalchemy import Column, Integer, String, ForeignKey
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
     # Связь с результатами тестов (если нужно)
    #test_results = relationship("UserTestResult", back_populates="user")


class Test(Base):
    __tablename__ = "tests"
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    # Связь с вопросами
   # questions = relationship("Question", back_populates="test")

class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, index=True)
    test_id = Column(Integer, ForeignKey("tests.id"))
    options1 = Column(String)
    options2 = Column(String)# JSON строка с вариантами ответов
    options3 = Column(String)
    options4 = Column(String)
    correct_answer = Column(String)
   # Связь с тестом
    #test = relationship("Test", back_populates="questions")

class UserTestResult(Base):
    __tablename__ = "user_test_results"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    test_id = Column(Integer, ForeignKey("tests.id"))
    score = Column(Integer)  # Количество правильных ответов

    # Связь с пользователем
    #user = relationship("User", back_populates="test_results")
    # Связь с тестом
    #test = relationship("Test")