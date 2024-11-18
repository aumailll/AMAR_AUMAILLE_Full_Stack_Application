from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.models.getdb import get_db
from api.services.anime import get_anime_data

# Initialiser le routeur
router = APIRouter(prefix="/anime", tags=["Anime"])

# Initialiser Jinja2 pour les templates
templates = Jinja2Templates(directory="api/templates")

@router.get("/")
def show_anime(request: Request, db: Session = Depends(get_db), format: str = "html"):
    """
    Affiche les données des animes depuis la base de données.
    """
    # Récupérer les données des animes via le service
    anime_list = get_anime_data(db)

    # Si format est JSON, renvoyer les données directement
    if format == "json":
        return JSONResponse(content=anime_list)

    # Sinon, rendre le template HTML
    return templates.TemplateResponse(
        "anime.html",
        {"request": request, "animes": anime_list}
    )

