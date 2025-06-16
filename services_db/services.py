import db.database as _database
import sqlalchemy.orm as _orm
import jwt as _jwt
import models.usr_model as _models
import schemas.usr_schema as _schema
import passlib.hash as _hash
from conf.config import settings

JWT_SECRET = settings.jwt_secret

def create_database():
    return _database.BASE.metadata.create_all(bind = _database.engine)

def get_user_by_email(email: str, db: _orm.Session):
    return db.query(_models.User).filter(_models.User.email == email).first()

def create_user(user: _schema.UserCreate, db: _orm.Session):
    user_obj = _models.User(
        email = user.email,
        hashed_password = _hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    db.commit()
    db.refresh(user_obj)
    return user_obj

def authenticate_user(email: str, password: str, db: _orm.Session):
    user = get_user_by_email(email,db)
    if not user:
        return False
    if not user.verify_password(password=password):
        return False
    return user

def create_token(user: _models.User):
    user_obj = _schema.User.model_validate(user)
    token = _jwt.encode(user_obj.model_dump(),JWT_SECRET)
    return dict(access_token = token,token_type="bearer")