from fastapi import APIRouter, Depends, Form, HTTPException, Request, Cookie
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
from api.models.getdb import get_db
from api.models.create_db import User
from api.services.auth import hash_password, verify_password, encode_jwt
import csv  # Si nécessaire pour la gestion des fichiers CSV

templates = Jinja2Templates(directory="api/templates")
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Route pour la page de connexion et d'inscription
@router.get("/")
def auth_page(request: Request):
    """Affiche la page unique pour connexion et inscription."""
    return templates.TemplateResponse("login.html", {"request": request})

# Route pour l'inscription de l'utilisateur
@router.post("/signup")
def signup(
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
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

    # Redirection vers la page de bienvenue avec un cookie contenant l'email
    response = RedirectResponse("/auth/welcome", status_code=303)
    response.set_cookie("email", email)  # Stocke l'email dans un cookie
    return response

# Route pour la connexion de l'utilisateur
@router.post("/login")
def login(
    email: str = Form(...), 
    password: str = Form(...), 
    db: Session = Depends(get_db)
):
    """Gère la connexion d'un utilisateur."""
    # Vérification des informations
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(password, db_user.password):
        raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")
    
    # Génération du token JWT (optionnel, pour authentification future)
    token = encode_jwt(str(db_user.id))
    
    # Création de la réponse de redirection vers la page de bienvenue
    response = RedirectResponse("/auth/welcome", status_code=303)
    
    # Enregistrement du token JWT dans un cookie (facultatif, si nécessaire)
    response.set_cookie("access_token", token)
    
    # Enregistrement de l'email dans un cookie
    response.set_cookie("email", email)  # Stocke l'email dans un cookie
    
    return response

# Route pour la page de bienvenue après la connexion
@router.get("/welcome")
def welcome_page(request: Request, email: str = Cookie(None)):
    """Affiche une page de bienvenue après la connexion"""
    if not email:
        raise HTTPException(status_code=401, detail="Non authentifié.")
    
    # Affiche la page de bienvenue avec l'email récupéré du cookie
    return templates.TemplateResponse("welcome.html", {"request": request, "email": email})

# Route pour afficher la base de données des utilisateurs
@router.get("/user_database")
def database_page(request: Request, db: Session = Depends(get_db)):
    """Affiche la base de données des utilisateurs"""
    users = db.query(User).all()  
    return templates.TemplateResponse("user_database.html", {"request": request, "users": users})

# Route pour afficher les animes depuis un fichier CSV
