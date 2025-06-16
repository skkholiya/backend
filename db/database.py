import sqlalchemy.ext.asyncio as _async_sql
import sqlalchemy.orm as _orm
import sqlalchemy.ext.declarative as _declarative
from conf.config import settings
from typing import AsyncGenerator

DATABASE_URL = "postgresql+asyncpg://postgres:toor@localhost:5432/usr_mobile_log"

# Create async engine using asyncpg
engine = _async_sql.create_async_engine(DATABASE_URL, echo=False)
print("Using DATABASE_URL:", DATABASE_URL)

# Async session factory
AsyncSessionLocal = _orm.sessionmaker(
    bind=engine,
    class_=_async_sql.AsyncSession,
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

# Base class for models
BASE = _declarative.declarative_base()

# Dependency for FastAPI routes
async def get_db() -> AsyncGenerator[_async_sql.AsyncSession, None]:
    async with AsyncSessionLocal() as session:
        yield session

'''
SYNC VERSION
'''
# import sqlalchemy as _sql
# import sqlalchemy.ext.declarative as _declarative
# import sqlalchemy.orm as _orm
# from conf.config import settings

# DATABASE_URL = settings.database_url

# engine = _sql.create_engine(DATABASE_URL)

# # MUST bind engine to sessionmaker
# SessionLocal = _orm.sessionmaker(
#     bind=engine,       
#     autoflush=False,
#     autocommit=False,
#     expire_on_commit=False
# )

# BASE = _declarative.declarative_base()

# # Dependency for FastAPI routes
# def get_db():
#     db = SessionLocal()
#     print(DATABASE_URL)
#     try:
#         yield db
#     finally:
#         db.close()