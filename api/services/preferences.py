from sqlalchemy.orm import Session
from fastapi import HTTPException
from api.models.create_db import User, UserAnime, Anime
from uuid import UUID 

# Services liés aux préférences des utilisateurs

# Pour notre barre de recherche d'anime
# On veut lister tous les animes qui s'approchent de la recherche d'un utilisateur 
# Ainsi, il pourra juste taper quelques lettres et trouver l'anime dans les résultats proposés
def search_anime(query: str, db: Session):
    """Recherche des animes correspondant à une requête."""
    return db.query(Anime).filter(Anime.titre.ilike(f"%{query}%")).all()


# Pour qu'un utilisateur ajoute un anime à sa liste qu'il pourra consulter ultérieurement
def add_anime_to_user(anime_rank: int, email: str, db: Session):
    """Ajoute un anime à la liste des préférences de l'utilisateur."""
    # Vérifie si l'utilisateur existe
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")

    # Vérifie si l'anime existe
    anime = db.query(Anime).filter(Anime.rank == anime_rank).first()  # Utilisation de rank comme identifiant
    if not anime:
        raise HTTPException(status_code=404, detail="Anime non trouvé.")
    
    # Vérifie si l'association existe déjà
    existing_entry = db.query(UserAnime).filter(
        UserAnime.user_id == user.id,  # Utilisation du UUID de l'utilisateur
        UserAnime.anime_rank == anime.rank  # Utilisation de rank comme clé primaire de anime
    ).first()
    
    if existing_entry:
        raise HTTPException(status_code=400, detail="Cet anime est déjà dans vos préférences.")
    
    # Ajouter l'anime à l'utilisateur
    new_entry = UserAnime(user_id=user.id, anime_rank=anime.rank)
    db.add(new_entry)
    db.commit()

    return {"message": "Anime ajouté avec succès."}


    # Ajoute l'anime aux préférences
    user_anime = UserAnime(user_id=user.id, anime_id=anime.id)
    db.add(user_anime)
    db.commit()
    

# Pour récupérer la liste d'anime de l'user connecté
def get_user_animes(user_id: UUID, db: Session):
    """Récupère les animes associés à un utilisateur via son id user :  UUID."""
    return (
        db.query(Anime)  # 
        .join(UserAnime)  # On effectue une jointure avec la table associative UserAnime
        .filter(UserAnime.user_id == user_id)  # On filtre les résultats pour ne garder que ceux liés à user_id
        .all()  
    )
