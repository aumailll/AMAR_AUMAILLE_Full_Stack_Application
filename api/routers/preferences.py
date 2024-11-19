from fastapi import APIRouter, Request, HTTPException, Depends, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from api.services.preferences import search_anime, add_anime_to_user
from api.models.getdb import get_db
from api.models.create_db import UserAnime , User, Anime
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="api/templates")
router = APIRouter(prefix="/preferences", tags=["Preferences"])

@router.get("/")
def preferences_page(request: Request, email: str = Cookie(None), query: str = "", db: Session = Depends(get_db)):
    """Page des préférences avec recherche d'anime et ajout à la base de données."""
    if not email:
        raise HTTPException(status_code=401, detail="Non authentifié.")
    
    results = []
    if query:
        results = search_anime(query, db)  # Recherche d'animes dans la base de données
    
    return templates.TemplateResponse("preferences.html", {
        "request": request, 
        "email": email, 
        "results": results,
        "query": query  # Pré-remplir la barre de recherche
    })

@router.post("/add_anime")
def add_anime_to_user_page(anime_id: int, email: str = Cookie(None), db: Session = Depends(get_db)):
    """Ajoute un anime sélectionné à la base de données de l'utilisateur."""
    if not email:
        raise HTTPException(status_code=401, detail="Non authentifié.")
    
    add_anime_to_user(anime_id, email, db)  # Ajout de l'anime à la base de données de l'utilisateur
    
    # Redirection vers la page pour voir les animes enregistrés
    return RedirectResponse(url="/preferences/show_database", status_code=303)

@router.get("/show_database")
def show_user_animes(request: Request, email: str = Cookie(None), db: Session = Depends(get_db)):
    """Affiche les animes enregistrés par l'utilisateur dans la base de données."""
    if not email:
        raise HTTPException(status_code=401, detail="Non authentifié.")
    
    # Récupération de l'utilisateur depuis son email
    user = db.query(User).filter(User.email == email).first()
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    
    # On récupère les animes associés à l'utilisateur
    user_animes = db.query(Anime).join(UserAnime).filter(UserAnime.user_id == user.id).all()
    
    return templates.TemplateResponse("show_preferences.html", {
        "request": request, 
        "email": email, 
        "user_animes": user_animes
    })
