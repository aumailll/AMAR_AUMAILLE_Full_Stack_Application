from pydantic import BaseModel
from typing import Optional

# Schéma pour l'ajout d'un anime à la liste de l'utilisateur
class UserAnimeCreate(BaseModel):
    """Schéma pour l'ajout d'un anime à la liste de l'utilisateur"""
    anime_rank: int  # L'ID ou le rank de l'anime
    email: str  # Email de l'utilisateur, pour lier l'anime à un utilisateur spécifique

    class Config:
        orm_mode = True

# Schéma pour afficher les animes préférés d'un utilisateur
class UserAnimeOut(BaseModel):
    """Schéma pour afficher les détails des animes d'un utilisateur"""
    rank: int  # Rank de l'anime
    titre: str  # Titre de l'anime
    score: float  # Score de l'anime
    episodes: int  # Nombre d'épisodes
    statut: str  # Statut de l'anime (en cours, terminé, etc.)
    studio: str  # Studio de production de l'anime
    producteurs: str  # Producteurs de l'anime
    type: Optional[str]  # Type de l'anime (peut être nul)
    genres_ET_themes: str  # Genres et thèmes associés

    class Config:
        orm_mode = True
