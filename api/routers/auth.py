# from fastapi import APIRouter, Depends, Form, HTTPException, Request, Cookie
# from fastapi.responses import RedirectResponse
# from fastapi.templating import Jinja2Templates
# from sqlalchemy.orm import Session
# from api.models.getdb import get_db
# from api.models.create_db import User
# from api.services.auth import hash_password, verify_password, encode_jwt
# import csv  #

# # Ici : les routes liées à la l'inscription, la connexion, l'authentification

# templates = Jinja2Templates(directory="api/templates")
# router = APIRouter(prefix="/auth", tags=["Authentication"])

# # Route pour la page de connexion et d'inscription
# @router.get("/") # directement à auth
# def auth_page(request: Request):
#     """Affiche la page unique pour connexion et inscription."""
#     return templates.TemplateResponse("login.html", {"request": request})

# # Route pour l'inscription de l'utilisateur
# @router.post("/signup")
# def signup(
#     email: str = Form(...), 
#     password: str = Form(...), 
#     db: Session = Depends(get_db)
# ):
#     """Gère l'inscription d'un utilisateur."""
#     # Vérification si l'email est déjà dans la base
#     db_user = db.query(User).filter(User.email == email).first()
#     if db_user:
#         raise HTTPException(status_code=400, detail="Email déjà utilisé.")

#     # Création de l'utilisateur
#     new_user = User(
#         email=email,
#         password=hash_password(password)
#     )
#     db.add(new_user)
#     db.commit()

#     # Redirection vers la page de bienvenue 
#     response = RedirectResponse("/auth/welcome", status_code=303)
#     response.set_cookie("email", email)  # Stocke l'email dans un cookie
#     return response


# # Route pour la connexion de l'utilisateur
# @router.post("/login")
# def login(
#     email: str = Form(...), 
#     password: str = Form(...), 
#     db: Session = Depends(get_db)
# ):
#     """Gère la connexion d'un utilisateur."""
#     # Vérification des informations : email correct (existant, bien écrit), mdp correct 
#     db_user = db.query(User).filter(User.email == email).first()
#     if not db_user or not verify_password(password, db_user.password):
#         raise HTTPException(status_code=401, detail="Email ou mot de passe incorrect.")
    
#     # Génération du token JWT
#     token = encode_jwt(str(db_user.id))
    
#     # Création de la réponse de redirection vers la page de bienvenue
#     response = RedirectResponse("/auth/welcome", status_code=303)
    
#     # Enregistrement du token JWT dans un cookie 
#     response.set_cookie("access_token", token)
    
#     # Enregistrement de l'email dans un cookie
#     response.set_cookie("email", email)  # Stocke l'email dans un cookie
    
#     return response

# # # Route pour la page de bienvenue après la connexion
# # @router.get("/welcome")
# # def welcome_page(request: Request, email: str = Cookie(None)):
# #     """Affiche une page de bienvenue après la connexion"""
# #     if not email:
# #         raise HTTPException(status_code=401, detail="Non authentifié.")
    
# #     # Affiche la page de bienvenue avec l'email récupéré du cookie
# #     return templates.TemplateResponse("welcome.html", {"request": request, "email": email})
# @router.get("/welcome/{email}")
# def welcome_page(request: Request, email: str, db: Session = Depends(get_db)):
#     """Affiche une page de bienvenue avec l'email dans l'URL"""
#     # Vérification si l'email existe dans la base
#     db_user = db.query(User).filter(User.email == email).first()
#     if not db_user:
#         raise HTTPException(status_code=404, detail="Utilisateur non trouvé.")
    
#     # Affiche la page avec l'email dans l'URL
#     return templates.TemplateResponse("welcome.html", {"request": request, "email": email})




# # Route pour afficher la base de données des utilisateurs
# @router.get("/user_database")
# def database_page(request: Request, db: Session = Depends(get_db)):
#     """Affiche la base de données des utilisateurs"""
#     users = db.query(User).all()  
#     return templates.TemplateResponse("user_database.html", {"request": request, "users": users})



from fastapi import APIRouter, Form, HTTPException, Depends, Request, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from api.models.create_db import User
from api.models.getdb import get_db
from api.services.auth import hash_password, verify_password, encode_jwt
from fastapi.templating import Jinja2Templates

templates = Jinja2Templates(directory="api/templates")
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Route pour afficher la page de connexion et d'inscription
@router.get("/")
def auth_page(request: Request):
    """Affiche la page unique pour connexion et inscription."""
    return templates.TemplateResponse("signup.html", {"request": request})

# Route pour l'inscription de l'utilisateur
@router.post("/signup")
def signup(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Gère l'inscription d'un utilisateur."""
    db_user = db.query(User).filter(User.email == email).first()
    if db_user:
        # Redirige vers la page d'erreur personnalisée
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Email déjà utilisé.",
            "detail": "Cet email est déjà enregistré dans notre base de données. Veuillez en choisir un autre."
        })
    
    new_user = User(email=email, password=hash_password(password))
    db.add(new_user)
    db.commit()
    
    response = RedirectResponse(f"/auth/login", status_code=303)
    response.set_cookie("email", email)
    return response


@router.get("/login")
def login_page(request: Request):
    """Affiche la page de connexion."""
    return templates.TemplateResponse("login.html", {"request": request})


# Route pour la connexion de l'utilisateur
@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Gère la connexion d'un utilisateur."""
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user or not verify_password(password, db_user.password):
        # Redirige vers la page d'erreur personnalisée
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Email ou mot de passe incorrect.",
            "detail": "Les informations que vous avez fournies ne correspondent à aucun compte. Veuillez vérifier vos identifiants."
        })
    
    response = RedirectResponse(f"/auth/welcome/{email}", status_code=303)
    response.set_cookie("email", email)
    return response

# Route pour la page de bienvenue
@router.get("/welcome/{email}")
def welcome_page(request: Request, email: str, db: Session = Depends(get_db)):
    """Affiche une page de bienvenue."""
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        # Redirige vers la page d'erreur personnalisée
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Utilisateur non trouvé.",
            "detail": "Aucun utilisateur n'a été trouvé avec cet email. Veuillez vérifier votre adresse email."
        })
    
    return templates.TemplateResponse("welcome.html", {"request": request, "email": email})

# Route pour afficher la base de données des utilisateurs
@router.get("/user_database")
def database_page(request: Request, email: str = Cookie(None), db: Session = Depends(get_db)):
    """Affiche la base de données des utilisateurs."""
    if not email:
        # Redirige vers la page d'erreur personnalisée
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Non authentifié.",
            "detail": "Vous devez être connecté pour accéder à cette page."
        })
    
    users = db.query(User).all()
    return templates.TemplateResponse("user_database.html", {"request": request, "users": users, "email": email})

# Route pour les préférences utilisateur
@router.get("/preferences/{email}")
def preferences_page(request: Request, email: str, db: Session = Depends(get_db)):
    """Affiche la page des préférences utilisateur."""
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        # Redirige vers la page d'erreur personnalisée
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Utilisateur non trouvé.",
            "detail": "Aucun utilisateur n'a été trouvé avec cet email. Veuillez vérifier votre adresse email."
        })
    
    # Exemple : récupérez des données personnalisées pour l'utilisateur ici
    return templates.TemplateResponse("preferences.html", {"request": request, "email": email})

# Route pour afficher la liste des animes
@router.get("/anime/{email}")
def show_anime(request: Request, email: str, db: Session = Depends(get_db)):
    """Affiche les animes."""
    db_user = db.query(User).filter(User.email == email).first()
    if not db_user:
        # Redirige vers la page d'erreur personnalisée
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Utilisateur non trouvé.",
            "detail": "Aucun utilisateur n'a été trouvé avec cet email. Veuillez vérifier votre adresse email."
        })
    
    # Exemple : récupérer les animes depuis la base ou une API
    animes = []  # Remplacez par les données réelles
    return templates.TemplateResponse("anime.html", {"request": request, "email": email, "animes": animes})
