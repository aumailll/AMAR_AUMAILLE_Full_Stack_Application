# schemas/anime.py
from pydantic import BaseModel
from typing import Optional
from uuid import UUID

#Vérification que les données correspondent aux types attendus
# Optional pour type car peut être nul

class AnimeOut(BaseModel):
    #id: UUID
    rank: int
    titre: str
    lien: str
    score: float
    episodes: int
    statut: str
    studio: str
    producteurs: str
    type: Optional[str]
    genres_ET_themes: str

    class Config:
        orm_mode = True
