from pydantic import BaseModel
from typing import Optional

# Schéma pour l'ajout d'un anime à la liste de l'utilisateur
class UserAnimeCreate(BaseModel):
    """Schéma pour l'ajout d'un anime à la liste de l'utilisateur"""
    anime_rank: int  # L'ID  = le rank de l'anime 
    email: str  # Email de l'utilisateur, pour lier l'anime à un utilisateur spécifique

    class Config:
        orm_mode = True

# Schéma pour afficher les animes préférés d'un utilisateur
class UserAnimeOut(BaseModel):
    """Schéma pour afficher les détails des animes d'un utilisateur"""
    rank: int 
    titre: str 
    score: float 
    episodes: int 
    statut: str  
    studio: str 
    producteurs: str  
    type: Optional[str] 
    genres_ET_themes: str  

    class Config:
        orm_mode = True
