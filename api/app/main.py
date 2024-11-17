from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette_exporter import PrometheusMiddleware, handle_metrics
from routers import auth
from models.database import engine, BaseSQL



async def lifespan(app: FastAPI):
    BaseSQL.metadata.create_all(bind=engine)
    yield

app = FastAPI(lifespan=lifespan)
# Inclure les routes de l'authentification
app.include_router(auth.router)
