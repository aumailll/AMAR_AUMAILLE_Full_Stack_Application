from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette_exporter import PrometheusMiddleware, handle_metrics
from api.routers import auth, anime, preferences
from api.models.getdb import engine, BaseSQL
from fastapi.responses import RedirectResponse
import os
from api.models.insert_data import insert_data 

# Fonction pour insérer les données après la création de la base de données
async def lifespan(app: FastAPI):
    # Créer toutes les tables à partir des modèles
    BaseSQL.metadata.create_all(bind=engine)
    
    # Insertion des données depuis le fichier CSV
    csv_file= r'Data/anime.csv'  
    insert_data(csv_file)
    
    yield

# Initialisation de l'application FastAPI
app = FastAPI(lifespan=lifespan)

@app.get("/", include_in_schema=False)  # On empêche d'afficher cette route dans la doc
async def redirect_to_login():
    return RedirectResponse(url="/auth/")

# Inclure les routes de l'authentification, anime et preferences 
app.include_router(auth.router)
app.include_router(anime.router)
app.include_router(preferences.router)


# Monter le répertoire statique et images nécessaires pour le bon fonctionnement de l'app
app.mount("/static", StaticFiles(directory="api/static"), name="static")
app.mount("/images", StaticFiles(directory="images"), name="images")

# Configuration des templates
templates = Jinja2Templates(directory="api/templates")
