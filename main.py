from fastapi import FastAPI, Request, Form, HTTPException
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.status import HTTP_302_FOUND
from sqlalchemy.exc import IntegrityError
from database import SessionLocal, engine
from models import Base, User
import random
import os
from contextlib import contextmanager
from fastapi import FastAPI, Request, Form, HTTPException, Depends
from fastapi.responses import RedirectResponse, HTMLResponse
from sqlalchemy.orm import Session

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

Base.metadata.create_all(bind=engine)

# Контекстный менеджер для работы с БД
@contextmanager
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    return templates.TemplateResponse("register.html", {"request": request})

@app.post("/register", response_class=HTMLResponse)
async def register(
    request: Request,
    first_name: str = Form(...),
    last_name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    with get_db() as db:
        try:
            # Проверяем, существует ли пользователь с таким email
            existing_user = db.query(User).filter(User.email == email).first()
            if existing_user:
                return templates.TemplateResponse(
                    "register.html",
                    {
                        "request": request,
                        "error": "Этот email уже зарегистрирован",
                        "first_name": first_name,
                        "last_name": last_name,
                        "email": email
                    }
                )
            
            # Создаем нового пользователя
            user = User(
                first_name=first_name,
                last_name=last_name,
                email=email,
                password=password  # В реальном приложении пароль должен быть хеширован!
            )
            
            db.add(user)
            db.commit()
            
            return RedirectResponse("/question1", status_code=HTTP_302_FOUND)
            
        except IntegrityError as e:
            db.rollback()
            return templates.TemplateResponse(
                "register.html",
                {
                    "request": request,
                    "error": "Произошла ошибка при регистрации",
                    "first_name": first_name,
                    "last_name": last_name,
                    "email": email
                }
            )
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=500, detail=str(e))

@app.get("/question1", response_class=HTMLResponse)
async def question1(request: Request):
    return templates.TemplateResponse("question1.html", {"request": request})

@app.get("/question2", response_class=HTMLResponse)
async def question2(request: Request):
    return templates.TemplateResponse("question2.html", {"request": request})

@app.get("/question3", response_class=HTMLResponse)
async def question3(request: Request, genre: str = None):
    if genre:
        print(f"Выбран жанр: {genre}")  # Можно сохранить в сессии/БД
    return templates.TemplateResponse("question3.html", {"request": request})

@app.get("/question4", response_class=HTMLResponse)
async def question4(request: Request):
    return templates.TemplateResponse("question4.html", {"request": request})

@app.get("/result", response_class=HTMLResponse)
async def result(request: Request):
    #toys = os.listdir("static/toys")
    #chosen = random.choice(toys)
    return templates.TemplateResponse(
        "result.html",
        {
            "request": request,
            #"toy": f"/static/toys/{chosen}"
        }
    )

