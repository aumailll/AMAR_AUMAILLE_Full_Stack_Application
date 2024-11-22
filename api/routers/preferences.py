from fastapi import APIRouter, Request, HTTPException, Depends, Cookie
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session
from api.services.preferences import search_anime, add_anime_to_user, get_user_animes
from api.models.getdb import get_db
from fastapi.templating import Jinja2Templates
from api.services.utils import validate_email_user
from fastapi import Form
from api.models.create_db import User

templates = Jinja2Templates(directory="api/templates")
router = APIRouter(prefix="/preferences", tags=["Preferences"])

from fastapi import HTTPException, status

@router.get("/{email}")
def preferences_page(
    request: Request, 
    email: User = Depends(validate_email_user),
    query: str = "", 
    db: Session = Depends(get_db)
):
    """
    Page des préférences avec recherche d'anime et ajout à la base de données.
    """
    try:
        results = []
        if query:
            results = search_anime(query, db)  # Appel au service de recherche
        return templates.TemplateResponse("preferences.html", {
            "request": request,
            "email": email.email,
            "results": results,
            "query": query
        })
    except HTTPException as e:
        # En cas d'erreur, on redirige avec un template error.html
        return templates.TemplateResponse(
            "error.html", 
            {
                "request": request, 
                "error_message": e.detail,  # Message d'erreur à afficher
                "detail": "Veuillez réessayer."  # Détails supplémentaires
            },
            status_code=e.status_code  # Code d'erreur HTTP
        )
    except Exception as ex:
        # Gestion d'autres exceptions imprévues
        return templates.TemplateResponse(
            "error.html", 
            {
                "request": request,
                "error_message": "Une erreur inattendue est survenue.",
                "detail": str(ex)  # Informations complémentaires
            },
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )





@router.post("/{email}/add_anime")
def add_anime(
    request: Request, 
    anime_rank: int = Form(...),  # Récupère anime_rank depuis un formulaire
    user :User = Depends(validate_email_user), 
    db: Session = Depends(get_db)
):
    try:
        # Ajouter l'anime aux préférences de l'utilisateur
        add_anime_to_user(anime_rank, user.email, db)
        
        # Retourner le template de succès
        return templates.TemplateResponse("ajout_anime.html", {"request": request, "email": user.email, "message": "Anime ajouté avec succès."})

    except HTTPException as e:
        # En cas d'erreur, on redirige avec un template error.html
        return templates.TemplateResponse(
            "error.html", 
            {
                "request": request, 
                "error_message": e.detail,  # Message d'erreur à afficher
                "detail": "Veuillez réessayer."  # Détails supplémentaires
            }
        )


@router.get("/{email}/show_preferences")
async def show_preferences(
    request: Request,
    user: User = Depends(validate_email_user),  # Directement valider l'utilisateur
    db: Session = Depends(get_db)
):
    user_animes = get_user_animes(user.id, db)  # On récupère les animes via l'UUID
    return templates.TemplateResponse(
        "show_preferences.html",
        {
            "request": request,
            "user_animes": user_animes,
            "email": user.email,  # Renvoyer l'email au template si nécessaire
        },
    )