# services/auth.py

from datetime import datetime, timedelta, timezone
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from jose import JWTError, jwt
from models.create_db import User
from schemas.user import UserCreate, UserLogin, UserOut
from schemas.token import Token
from typing import Optional
from fastapi import HTTPException, status

# Configuration du contexte de hachage pour le mot de passe
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Clé secrète pour le JWT
SECRET_KEY = "abcdefgh"
ALGORITHM = "HS256"

# Durée de validité du token (90 minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = 90

def hash_password(password: str) -> str:
    """Hache le mot de passe avant de le stocker"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie que le mot de passe donné correspond au mot de passe haché"""
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)) -> str:
    """Crée un token JWT avec une date d'expiration"""
    expire = datetime.now(tz=timezone.utc) + expires_delta
    to_encode = data.copy()
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    """Récupère un utilisateur à partir de son email"""
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user: UserCreate) -> User:
    """Crée un nouvel utilisateur dans la base de données"""
    db_user = User(email=user.email, username=user.username, password=hash_password(user.password))
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def verify_token(token: str, credentials_exception) -> dict:
    """Vérifie la validité du token JWT"""
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        return {"email": email, "exp": payload.get("exp")}
    except JWTError:
        raise credentials_exception

def get_current_user(db: Session, token: str) -> Optional[User]:
    """Récupère l'utilisateur courant à partir du token"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token is invalid or expired",
        headers={"WWW-Authenticate": "Bearer"},
    )
    token_data = verify_token(token, credentials_exception)
    return get_user_by_email(db, token_data["email"])
