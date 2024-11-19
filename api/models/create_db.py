from sqlalchemy import Column, Integer, String, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.models.getdb import BaseSQL
import uuid
import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/db_projet")

class User(BaseSQL):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relationship: un utilisateur peut avoir plusieurs préférences d'anime
    preferences = relationship("UserAnime", back_populates="user", cascade="all, delete-orphan")

class Anime(BaseSQL):
    __tablename__ = 'anime'
    rank = Column(Integer, primary_key=True)  # Utilisation de rank comme clé primaire
    titre = Column(String)
    score = Column(Float)
    episodes = Column(Integer)
    statut = Column(String)
    studio = Column(String, nullable=True)
    producteurs = Column(String, nullable=True)
    type = Column(String, nullable=True)
    genres_themes = Column(String)
    lien = Column(String)

    # Relationship: anime peut avoir plusieurs préférences associées
    preferences = relationship("UserAnime", back_populates="anime")

class UserAnime(BaseSQL):
    __tablename__ = 'user_anime'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)  # Clé étrangère pour user
    anime_rank = Column(Integer, ForeignKey('anime.rank'), primary_key=True)  # Clé étrangère pour anime

    # Définir la clé primaire combinée
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'anime_rank'),
    )

    user = relationship("User", back_populates="preferences")
    anime = relationship("Anime", back_populates="preferences")
