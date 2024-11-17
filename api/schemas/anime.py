# schemas/anime.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

class AnimeOut(BaseModel):
    """Schéma pour l'affichage des anime"""
    id: UUID
    rank: int
    titre: str
    lien: str
    score: float
    episodes: Optional[int]
    statut: Optional[str]
    studio: Optional[str]
    producteurs: Optional[str]
    type: Optional[str]
    genres_ET_themes: str

    class Config:
        orm_mode = True
