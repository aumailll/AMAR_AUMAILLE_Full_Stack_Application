from sqlalchemy import Column, Integer, String, Float, ForeignKey
import os
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.models.database import BaseSQL

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/db_projet")

class User(BaseSQL):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(255), unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    # Relationship: un utilisateur peut avoir plusieurs préférences d'anime
    preferences = relationship("UserAnimePreferences", back_populates="user", cascade="all, delete-orphan")

class Anime(BaseSQL):
    __tablename__ = 'anime'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    rank = Column(Integer)
    titre = Column(String(255))
    lien = Column(String(1000))
    score = Column(Float)
    episodes = Column(Integer)
    statut = Column(String(100))
    studio = Column(String(255), nullable=True)
    producteurs = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    genres_ET_themes = Column(String)

    # Relationship: anime peut avoir plusieurs préférences associées
    preferences = relationship("UserAnimePreferences", back_populates="anime")

class UserAnimePreferences(BaseSQL):
    __tablename__ = 'user_anime_preferences'
    id = Column(UUID(as_uuid=True), primary_key=True, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id', ondelete='CASCADE'))
    anime_id = Column(UUID(as_uuid=True), ForeignKey('anime.id', ondelete='CASCADE'))
    min_score = Column(Float, nullable=True)  # Score minimum sélectionné
    pref_genre_theme = Column(String, nullable=True)  # Genre/Thème préféré

    user = relationship("User", back_populates="preferences")
    anime = relationship("Anime", back_populates="preferences")

# Créer les tables dans la base de données
# Base.metadata.create_all(bind=engine)
