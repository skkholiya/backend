import sqlalchemy as _sql
import sqlalchemy.ext.declarative as _declarative
import sqlalchemy.orm as _orm
from conf.config import settings

DATABASE_URL = settings.database_url

engine = _sql.create_engine(DATABASE_URL)

# MUST bind engine to sessionmaker
SessionLocal = _orm.sessionmaker(
    bind=engine,       
    autoflush=False,
    autocommit=False,
    expire_on_commit=False
)

BASE = _declarative.declarative_base()

# Dependency for FastAPI routes
def get_db():
    db = SessionLocal()
    print(DATABASE_URL)
    try:
        yield db
    finally:
        db.close()