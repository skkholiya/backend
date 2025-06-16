import db.database as _database
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import jwt as _jwt
import models.usr_model as _models
import schemas.usr_schema as _schema
import fastapi.security as _security
import passlib.hash as _hash
from conf.config import settings
import fastapi as _fastapi

JWT_SECRET = settings.jwt_secret
get_token = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

# -------------------------
# Create Tables (Async)
# -------------------------
async def create_database():
    async with _database.engine.begin() as conn:
        await conn.run_sync(_database.BASE.metadata.create_all)

# -------------------------
# Get User by Email
# -------------------------
async def get_user_by_email(email: str, db: AsyncSession):
    stmt = select(_models.User).where(_models.User.email == email)
    result = await db.execute(stmt)
    return result.scalar_one_or_none()

# -------------------------
# Create User
# -------------------------
async def create_user(user: _schema.UserCreate, db: AsyncSession):
    user_obj = _models.User(
        email=user.email,
        hashed_password=_hash.bcrypt.hash(user.hashed_password)
    )
    db.add(user_obj)
    await db.commit()
    await db.refresh(user_obj)
    return user_obj

# -------------------------
# Authenticate User
# -------------------------
async def authenticate_user(email: str, password: str, db: AsyncSession):
    user = await get_user_by_email(email, db)
    if not user or not user.verify_password(password):
        return False
    return user

# -------------------------
# Create JWT Token
# -------------------------
def create_token(user: _models.User):
    user_obj = _schema.User.model_validate(user)
    token = _jwt.encode(user_obj.model_dump(), JWT_SECRET, algorithm="HS256")
    return {"access_token": token, "token_type": "bearer"}

# -------------------------
# Get Current User from JWT
# -------------------------
async def get_current_user(
    db: AsyncSession = _fastapi.Depends(_database.get_db),
    token: str = _fastapi.Depends(get_token)
):
    try:
        payload = _jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
        stmt = select(_models.User).where(_models.User.id == payload["id"])
        result = await db.execute(stmt)
        user = result.scalar_one_or_none()
        if user is None:
            raise
    except:
        raise _fastapi.HTTPException(status_code=401, detail="Invalid username or password!!")

    return _schema.User.model_validate(user)


'''
SYNC VERSION
'''
# import db.database as _database
# import sqlalchemy.orm as _orm
# import jwt as _jwt
# import models.usr_model as _models
# import schemas.usr_schema as _schema
# import fastapi.security as _security
# import passlib.hash as _hash
# from conf.config import settings
# import fastapi as _fastapi

# JWT_SECRET = settings.jwt_secret
# get_token = _security.OAuth2PasswordBearer(tokenUrl="/api/token")

# def create_database():
#     return _database.BASE.metadata.create_all(bind = _database.engine)

# def get_user_by_email(email: str, db: _orm.Session):
#     return db.query(_models.User).filter(_models.User.email == email).first()

# def create_user(user: _schema.UserCreate, db: _orm.Session):
#     user_obj = _models.User(
#         email = user.email,
#         hashed_password = _hash.bcrypt.hash(user.hashed_password)
#     )
#     db.add(user_obj)
#     db.commit()
#     db.refresh(user_obj)
#     return user_obj

# def authenticate_user(email: str, password: str, db: _orm.Session):
#     user = get_user_by_email(email,db)
#     if not user:
#         return False
#     if not user.verify_password(password=password):
#         return False
#     return user

# def create_token(user: _models.User):
#     user_obj = _schema.User.model_validate(user)
#     token = _jwt.encode(user_obj.model_dump(),JWT_SECRET)
#     return dict(access_token = token,token_type="bearer")

# def get_current_user(db: _orm.Session = _fastapi.Depends(_database.get_db), 
#                      token: str = _fastapi.Depends(get_token)):
#     try:
#         payload = _jwt.decode(token,JWT_SECRET,algorithms=["HS256"])
#         user = db.query(_models.User).get(payload['id'])
#     except:
#         raise _fastapi.HTTPException(status_code=401, detail="Invalid username or password!!")
    
#     return _schema.User.model_validate(user)