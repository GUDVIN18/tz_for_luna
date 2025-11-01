from fastapi import FastAPI
from app.router import router
from core.db.database import engine
from core.db.tables import metadata

app = FastAPI(
    title="Microservice TZ",
    version="0.1.0",
    openapi_tags=[{"name": "Организации", "description": "Работа с организациями"}],
)
app.include_router(router)