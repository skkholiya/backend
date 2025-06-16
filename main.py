# app/main.py
import fastapi as _fastapi
from fastapi import FastAPI
from sqlalchemy.orm import Session
import db.database as _database
import fastapi.security as _security
import services_db.services as _services
import schemas.usr_schema as _schema
from contextlib import asynccontextmanager

@asynccontextmanager
async def lifespan(app: FastAPI):
    _services.create_database()
    yield

app = FastAPI(lifespan=lifespan)

@app.post("/api/users")
def create_user(user: _schema.UserCreate, db:Session=_fastapi.Depends(_database.get_db)):
    db_user = _services.get_user_by_email(user.email,db)
    if db_user:
        raise _fastapi.HTTPException(status_code=400, detail="Email already in use")
    return _services.create_user(user,db)

@app.post("/api/token")
def generate_token(
    form_data: _security.OAuth2PasswordRequestForm=_fastapi.Depends(),
    db: Session=_fastapi.Depends(_database.get_db)
):
    user = _services.authenticate_user(form_data.username,form_data.password,db)
    if not user:
        raise _fastapi.HTTPException(status_code=401,detail="Invalid credentials!!")
    return _services.create_token(user)

@app.get("/api/users/me",response_model=_schema.User)
def get_user(user:_schema.User= _fastapi.Depends(_services.get_current_user)):
    return user

@app.get("/")
def root(db: Session = _fastapi.Depends(_database.get_db)):
    return {"message": "DB connected!"}
