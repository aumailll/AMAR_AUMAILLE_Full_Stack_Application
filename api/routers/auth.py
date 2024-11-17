from fastapi import APIRouter, Depends, Form, HTTPException, Request
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from api.models.getdb import get_db
from api.models.create_db import User
from api.services.auth import hash_password, verify_password, encode_jwt
#import logging #nouveau fct pas 
import csv # nouveau

templates = Jinja2Templates(directory="api/templates")
router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.get("/")
def auth_page(request: Request):
    """Affiche la page unique pour connexion et inscription."""
    return templates.TemplateResponse("login.html", {"request": request})

@router.post("/signup")
def signup(
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    # logging.info(f"Email inscription: {email}, Mot de passe inscription: {password}") # j'aime bien l'idée mais ça ne fct pas
    """Gère l'inscription d'un utilisateur."""
    # Vérification si l'email est déjà dans la base
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        raise HTTPException(status_code=400, detail="Email déjà utilisé.")

    # Création de l'utilisateur
    new_user = User(
        email=email,
        password=hash_password(password)
    )
    db.add(new_user)
    db.commit()
    return RedirectResponse("/auth/", status_code=303)

@router.post("/login")
def login(
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    # logging.info(f"Email login: {email}, Mot de passe login: {password}") # j'aime bien l'idée mais ça ne fct pas
    """Gère la connexion d'un utilisateur."""
    # Vérification des informations
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")
    
    # AVANT GIULIA : 
    # # Génération du token JWT
    # token = encode_jwt(str(db_user.id))
    # response = RedirectResponse("/", status_code=303)
    # response.set_cookie("access_token", token)
    # return response
    # Génération du token JWT
    token = encode_jwt(str(db_user.id))
    response = RedirectResponse(f"/auth/welcome?email={email}", status_code=303)
    response.set_cookie("access_token", token)
    return response

# NOUVEAU
@router.get("/welcome")
def welcome_page(request: Request, email: str):
    """Affiche une page de bienvenue après connexion."""
    return templates.TemplateResponse("welcome.html", {"request": request, "email": email})

@router.get("/user_database")
def database_page(request: Request, db: Session = Depends(get_db)):
    """Affiche la base de données usager du projet."""
    users = db.query(User).all()  
    return templates.TemplateResponse("user_database.html", {"request": request, "users": users})


# # Route pour afficher les animes
# @router.get("/anime")
# def show_anime(request: Request):
#     """Affiche les données des animes depuis le fichier CSV."""
#     anime_list = []
#     csv_file_path = "Data/anime.csv"  # Chemin du fichier CSV
#     try:
#         with open(csv_file_path, newline='', encoding='utf-8') as csvfile:
#             reader = csv.DictReader(csvfile)
#             for row in reader:
#                 anime_list.append(row)
#     except FileNotFoundError:
#         raise HTTPException(status_code=404, detail="Fichier CSV introuvable.")
    
#     return templates.TemplateResponse("anime.html", {"request": request, "animes": anime_list})

from sqlalchemy.sql import text  # Importez text pour exécuter des requêtes brutes

# @router.get("/anime")
# def show_anime(request: Request, db: Session = Depends(get_db)):
#     """Affiche les données des animes depuis la base de données."""
#     query = text("SELECT * FROM anime")  # Utilisation explicite de text()
#     animes = db.execute(query).fetchall()
#     return templates.TemplateResponse("anime.html", {"request": request, "animes": animes})
from sqlalchemy.sql import text  # Importez text

@router.get("/anime")
def show_anime(db: Session = Depends(get_db)):
    animes = db.execute(text("SELECT * FROM anime")).fetchall()

    custom_columns = ["Rang", "Titre", "Score", "Episodes", "Statut", "Studio", "Producteurs", "Type", "Genres_ET_Themes", "Lien"]
    anime_list = [
        dict(zip(custom_columns, anime))
        for anime in animes
    ]

    return templates.TemplateResponse(
        "anime.html",
        {"request": {}, "animes": anime_list}
    )
