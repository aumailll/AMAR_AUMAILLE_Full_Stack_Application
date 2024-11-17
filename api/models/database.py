'''from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os 


POSTGRES_USER = os.environ.get("user")
POSTGRES_PASSWORD = os.environ.get("password")
POSTGRES_DB = os.environ.get("db_projet")


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/db_projet")
print(DATABASE_URL)

engine = create_engine(
    DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

BaseSQL = declarative_base()'''