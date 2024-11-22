
from fastapi import APIRouter, Form,  Depends, Request, Cookie
from fastapi.responses import RedirectResponse
from sqlalchemy.orm import Session
from api.models.create_db import User
from api.models.getdb import get_db
from api.services.auth import hash_password, verify_password, encode_jwt
from fastapi.templating import Jinja2Templates

# Route pour accéder à la page d'inscription (puis de connexion ensuite)
templates = Jinja2Templates(directory="api/templates")
router = APIRouter(prefix="/auth", tags=["Authentication"])

# Dès le lancement de l'app, on affiche la page d'inscription
@router.get("/")
def auth_page(request: Request):
    """Affiche la page unique pour connexion et inscription."""
    return templates.TemplateResponse("signup.html", {"request": request})

# Route pour que l'utilisateur rentre ses informations d'inscription
@router.post("/signup")
def signup(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Gère l'inscription d'un utilisateur."""
    db_user = db.query(User).filter(User.email == email).first()
    if db_user: # si l'email existe déjà dans notre bdd
        # Redirige vers la page d'erreur personnalisée
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Email déjà utilisé.",
            "detail": "Cet email est déjà enregistré dans notre base de données. Veuillez en choisir un autre."
        })
    
    # Si tout se passe bien, l'user est ajouté à la table user
    new_user = User(email=email, password=hash_password(password))
    db.add(new_user)
    db.commit()
    
    # Dans ce cas, il est redirigé vers la page de connexion
    # Nous avons imposé la connexion pour tester facilement l'authentification surtout
    response = RedirectResponse(f"/auth/login", status_code=303)
    response.set_cookie("email", email)
    return response


# Route pour accéder à la page de connexion
@router.get("/login")
def login_page(request: Request):
    """Affiche la page de connexion."""
    return templates.TemplateResponse("login.html", {"request": request})


# Pour que l'utilisateur insère ses informations de connexion 
@router.post("/login")
def login(request: Request, email: str = Form(...), password: str = Form(...), db: Session = Depends(get_db)):
    """Gère la connexion d'un utilisateur."""
    db_user = db.query(User).filter(User.email == email).first() # vérification de l'email 
    if not db_user or not verify_password(password, db_user.password): # vérification que le mot de passe est ok pour ce mail
        # Redirige vers la page d'erreur personnalisée
        return templates.TemplateResponse("error.html", {
            "request": request,
            "error_message": "Email ou mot de passe incorrect.",
            "detail": "Les informations que vous avez fournies ne correspondent à aucun compte. Veuillez vérifier vos identifiants."
        })
    
    # Si tout se passe bien, redirection vers la page de bienvenue
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




