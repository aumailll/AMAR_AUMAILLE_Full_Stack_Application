from sqlalchemy.orm import Session
from api.models.create_db import Anime, UserAnime, User  # Assure-toi de définir cette table de relation UserAnime
from fastapi import  HTTPException

def search_anime(query: str, db: Session):
    """Recherche un anime dans la base de données selon le titre."""
    results = db.query(Anime).filter(Anime.title.ilike(f"%{query}%")).all()
    return results

def add_anime_to_user(anime_id: int, user_email: str, db: Session):
    """Ajoute un anime à la liste d'un utilisateur."""
    user = db.query(User).filter(User.email == user_email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    
    anime = db.query(Anime).filter(Anime.id == anime_id).first()
    if not anime:
        raise HTTPException(status_code=404, detail="Anime non trouvé.")
    
    user_anime = UserAnime(user_id=user.id, anime_id=anime.id)
    db.add(user_anime)
    db.commit()
    return anime
