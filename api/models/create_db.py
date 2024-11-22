from sqlalchemy import Column, Integer, String, Float, ForeignKey, PrimaryKeyConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from api.models.getdb import BaseSQL
import uuid
import os

#Ici, on crée les tables : User pour les utilisateurs, Anime pour les anime et UserAnime pour les préférences
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@db:5432/db_projet")

# User doit posséder un email valide et un mot de passe qui sera haché par sécurité 
class User(BaseSQL):
    __tablename__ = 'users'
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)

    # Relationship: un utilisateur peut avoir plusieurs préférences d'anime
    preferences = relationship("UserAnime", back_populates="user", cascade="all, delete-orphan")


# Anime garde toutes les caractéristiques définies dans le csv
# On utilise rank en id car c'est une valeur unique et incrémentée donc ça convient totalement pour un id 
class Anime(BaseSQL):
    __tablename__ = 'anime'
    rank = Column(Integer, primary_key=True)  # Utilisation de rank comme clé primaire
    titre = Column(String)
    score = Column(Float)
    episodes = Column(Integer)
    statut = Column(String)
    studio = Column(String)
    producteurs = Column(String)
    type = Column(String, nullable=True) # Parfois ce n'est pas mentionné donc on autorise les valeurs manquantes
    genres_themes = Column(String)
    lien = Column(String)

    # Relationship: anime peut être aimé par plusieurs utilisateurs
    preferences = relationship("UserAnime", back_populates="anime")


# Pour gérer les préférences de chaque user
# L'objectif est de sauvegarder les animes préférés d'un user défini ici 
class UserAnime(BaseSQL):
    __tablename__ = 'user_anime'
    
    user_id = Column(UUID(as_uuid=True), ForeignKey('users.id'), primary_key=True)  # Clé étrangère pour user
    anime_rank = Column(Integer, ForeignKey('anime.rank'), primary_key=True)  # Clé étrangère pour anime

    # On crée une clé combinée 
    __table_args__ = (
        PrimaryKeyConstraint('user_id', 'anime_rank'),
    )

    user = relationship("User", back_populates="preferences")
    anime = relationship("Anime", back_populates="preferences")
