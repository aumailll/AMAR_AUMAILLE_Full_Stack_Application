from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
import os

#onfigure une connexion à une base de données PostgreSQL avec SQLAlchemy
# On utilise les mêmes infos que dans le Docker compose pour bien se connecter 
POSTGRES_USER = os.environ.get("user")
POSTGRES_PASSWORD = os.environ.get("password")
POSTGRES_DB = os.environ.get("db_projet")


DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@postgres:5432/db_projet")


print(DATABASE_URL)

# Pour établir la communication avec la bdd 
engine = create_engine(
    DATABASE_URL
)

# Création de la session pour gérer les interactions
# Session liée à l'engine créé au-dessus 
SessionLocal = sessionmaker(autocommit=False, autoflush=True, bind=engine)

BaseSQL = declarative_base()

# Gestion de la connexion sécurisée 
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
