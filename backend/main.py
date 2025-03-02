from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.staticfiles import StaticFiles
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from sqlalchemy.orm import Session
from datetime import timedelta
from . import models, schemas, crud, auth
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.mount("/site", StaticFiles(directory="frontend"))

# Добавление CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


@app.post("/register/", response_model=schemas.User)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)

@app.post("/token/", response_model=schemas.Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = crud.get_user_by_username(db, username=form_data.username)
    if not user or not auth.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=auth.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = auth.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.get("/users/me/", response_model=schemas.User)
def read_users_me(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    username = auth.get_username_from_token(token)
    if username is None:
        raise credentials_exception
    user = crud.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user

@app.get("/tests/", response_model=list[schemas.Test])
def read_tests(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    tests = db.query(models.Test).offset(skip).limit(limit).all()
    return tests

@app.get("/tests/{test_id}/questions/", response_model=list[schemas.Question])
def read_questions(test_id: int, db: Session = Depends(get_db)):
    questions = db.query(models.Question).filter(models.Question.test_id == test_id).all()
    return questions


@app.get("/tests/{test_id}/questions/", response_model=list[schemas.Question])
def read_questions(test_id: int, db: Session = Depends(get_db)):
    questions = db.query(models.Question).filter(models.Question.test_id == test_id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="Вопросы не найдены")
    return questions

# Отправка ответов на тест
@app.post("/tests/{test_id}/submit/")
def submit_test(test_id: int, answers: schemas.TestAnswers, db: Session = Depends(get_db)):
    questions = db.query(models.Question).filter(models.Question.test_id == test_id).all()
    if not questions:
        raise HTTPException(status_code=404, detail="Тест не найден")

    correct_answers = 0
    for question in questions:
        if question.correct_answer == answers.answers.get(str(question.id)):
            correct_answers += 1

    return {"correct_answers": correct_answers, "total_questions": len(questions)}
