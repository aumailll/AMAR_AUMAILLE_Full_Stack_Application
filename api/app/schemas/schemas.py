from pydantic import BaseModel, EmailStr
from uuid import UUID
from typing import Optional


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: UUID
    username: str
    email: EmailStr

    class Config:
        orm_mode = True

class Token(BaseModel):
    access_token: str
    token_type: str

class AnimeOut(BaseModel):
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