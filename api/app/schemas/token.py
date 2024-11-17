# schemas/token.py
from pydantic import BaseModel

class Token(BaseModel):
    """Schéma pour le token JWT généré lors de la connexion"""
    access_token: str
    token_type: str
