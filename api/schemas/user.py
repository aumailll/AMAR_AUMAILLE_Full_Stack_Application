# schemas/user.py
from pydantic import BaseModel, EmailStr
from uuid import UUID

# Vérification que les données insérées et affichées sont conformes aux types attendus

class UserCreate(BaseModel):
    """Schéma pour la création d'un utilisateur"""
    #username: str
    email: EmailStr #on vérifie que c'est bien un email
    password: str

class UserLogin(BaseModel):
    """Schéma pour la connexion d'un utilisateur"""
    email: EmailStr
    password: str

class UserOut(BaseModel):
    """Schéma pour l'affichage des détails d'un utilisateur après connexion"""
    id: UUID
    #username: str
    email: EmailStr

    class Config:
        orm_mode = True
