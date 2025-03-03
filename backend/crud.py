'''from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    fake_hashed_password = user.password + "notreallyhashed"
    db_user = models.User(username=user.username, hashed_password=fake_hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
    
    
    
    
from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

# Функции для работы с пользователями

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Функции для работы с тестами

def get_test(db: Session, test_id: int):
    return db.query(models.Test).filter(models.Test.id == test_id).first()

def get_tests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Test).offset(skip).limit(limit).all()

def create_test(db: Session, test: schemas.TestCreate):
    db_test = models.Test(title=test.title, description=test.description)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

# Функции для работы с вопросами

def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()

def get_questions_by_test(db: Session, test_id: int):
    return db.query(models.Question).filter(models.Question.test_id == test_id).all()

def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(
        text=question.text,
        options=question.options,
        correct_answer=question.correct_answer,
        test_id=question.test_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# Функции для работы с результатами тестов

def get_user_test_result(db: Session, result_id: int):
    return db.query(models.UserTestResult).filter(models.UserTestResult.id == result_id).first()

def get_user_test_results(db: Session, user_id: int):
    return db.query(models.UserTestResult).filter(models.UserTestResult.user_id == user_id).all()

def create_user_test_result(db: Session, result: schemas.UserTestResultCreate):
    db_result = models.UserTestResult(
        user_id=result.user_id,
        test_id=result.test_id,
        score=result.score
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result'''
    
    
from sqlalchemy.orm import Session
from . import models, schemas
from .auth import get_password_hash

# Функции для работы с пользователями

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_username(db: Session, username: str):
    return db.query(models.User).filter(models.User.username == username).first()

def create_user(db: Session, user: schemas.UserCreate):
    hashed_password = get_password_hash(user.password)
    db_user = models.User(username=user.username, hashed_password=hashed_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

# Функции для работы с тестами

def get_test(db: Session, test_id: int):
    return db.query(models.Test).filter(models.Test.id == test_id).first()

def get_tests(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Test).offset(skip).limit(limit).all()

def create_test(db: Session, test: schemas.TestCreate):
    db_test = models.Test(title=test.title, description=test.description)
    db.add(db_test)
    db.commit()
    db.refresh(db_test)
    return db_test

# Функции для работы с вопросами

def get_question(db: Session, question_id: int):
    return db.query(models.Question).filter(models.Question.id == question_id).first()

def get_questions_by_test(db: Session, test_id: int):
    return db.query(models.Question).filter(models.Question.test_id == test_id).all()

def create_question(db: Session, question: schemas.QuestionCreate):
    db_question = models.Question(
        text=question.text,
        options1=question.options1,
        options2=question.options2,
        options3=question.options3,
        options4=question.options4,
        correct_answer=question.correct_answer,
        test_id=question.test_id
    )
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    return db_question

# Функции для работы с результатами тестов

def get_user_test_result(db: Session, result_id: int):
    return db.query(models.UserTestResult).filter(models.UserTestResult.id == result_id).first()

def get_user_test_results(db: Session, user_id: int):
    return db.query(models.UserTestResult).filter(models.UserTestResult.user_id == user_id).all()

def create_user_test_result(db: Session, result: schemas.UserTestResultCreate):
    db_result = models.UserTestResult(
        user_id=result.user_id,
        test_id=result.test_id,
        score=result.score
    )
    db.add(db_result)
    db.commit()
    db.refresh(db_result)
    return db_result

# Функция для проверки ответов пользователя и расчета результата теста

def calculate_test_score(db: Session, user_answers: dict, test_id: int):
    """
    Функция для расчета результата теста на основе ответов пользователя.
    :param db: Сессия базы данных.
    :param user_answers: Словарь с ответами пользователя (ключ - ID вопроса, значение - выбранный ответ).
    :param test_id: ID теста.
    :return: Количество правильных ответов.
    """
    questions = get_questions_by_test(db, test_id)
    correct_answers = 0

    for question in questions:
        if str(question.id) in user_answers:
            user_answer = user_answers[str(question.id)]
            # Сравниваем ответ пользователя с правильным ответом
            if user_answer == question.correct_answer:
                correct_answers += 1

    return correct_answers