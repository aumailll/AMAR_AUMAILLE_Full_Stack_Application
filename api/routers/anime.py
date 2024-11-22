from fastapi import APIRouter, Depends, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.models.getdb import get_db
from api.services.anime import get_anime_data
from api.services.utils import validate_email_user

# Router anime associé au service anime 
# L'URL débutera par /anime (après local host...)  
router = APIRouter(prefix="/anime", tags=["Anime"])
templates = Jinja2Templates(directory="api/templates")

@router.get("/{email}")
def show_anime(request: Request, email: str = Depends(validate_email_user), db: Session = Depends(get_db), format: str = "html"):
    """
    Affiche les données des animes depuis la base de données.
    """
    # On récupère les données des animes via le service anime.py
    anime_list = get_anime_data(db)

   
    #if format == "json":
        #return JSONResponse(content=anime_list)

    # Retourner l'affichage des animes avec l'email
    return templates.TemplateResponse(
        "anime.html",
        {"request": request, "animes": anime_list, "email": email.email}
    )
