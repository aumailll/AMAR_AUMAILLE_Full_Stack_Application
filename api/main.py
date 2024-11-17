from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette_exporter import PrometheusMiddleware, handle_metrics
from api.routers import auth
from api.models.getdb import engine, BaseSQL
from fastapi.responses import RedirectResponse

async def lifespan(app: FastAPI):
    BaseSQL.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
@app.get("/", include_in_schema=False)  # On empêche d'afficher cette route dans la doc
async def redirect_to_login():
    return RedirectResponse(url="/auth/")

# Inclure les routes de l'authentification
app.include_router(auth.router)

# Monter le répertoire statique
app.mount("/static", StaticFiles(directory="api/static"), name="static")

# Configuration des templates
templates = Jinja2Templates(directory="api/templates")
