from passlib.context import CryptContext
import jwt
import os
from datetime import datetime, timedelta, timezone 

# Services liés à l'authentification 

# Contexte pour le hachage des mots de passe
# Moyen de sécuriser les mdp 
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

#CLé stockée dans une variable d'environnement comme suggérée dans le cours 
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "notre_key")
JWT_SECRET_ALGORITHM = os.getenv("JWT_SECRET_ALGORITHM", "HS256")

def hash_password(password: str) -> str:
    """Hachage d'un mot de passe"""
    return pwd_context.hash(password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Vérifie si un mot de passe correspond à son hash"""
    return pwd_context.verify(plain_password, hashed_password)

# Génération du token et validation pour l'authentification réussie et sécurisé
def encode_jwt(user_id: str) -> str:
    """Génère un token JWT"""
    expiration = datetime.now(tz=timezone.utc)  + timedelta(hours=2)  # Expire après 2 heures
    payload = {"user_id": user_id, "exp": expiration}
    return jwt.encode(payload, JWT_SECRET_KEY, algorithm=JWT_SECRET_ALGORITHM)

def decode_jwt(token: str) -> dict:
    """Décode un token JWT"""
    return jwt.decode(token, JWT_SECRET_KEY, algorithms=[JWT_SECRET_ALGORITHM])

