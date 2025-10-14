from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordBearer , OAuth2PasswordRequestForm
from app.api.v1.api import api_router
from app.db.session import create_db_and_tables
import logging

logger = logging.getLogger(__name__)

app = FastAPI()

app = FastAPI(title="Sistema Bancario API")

def safe_create_db_and_tables():
    try:
        
        # create_db_and_tables()
        logger.info("✅ Tablas creadas o ya existentes.")
    except Exception as e:
        logger.warning(f"⚠️ No se pudo conectar a la base de datos al iniciar: {e}")
        
@app.on_event("startup")
def on_startup():
    # Esta línea crea las tablas en la base de datos si no existen
    # En un entorno de producción, se suele usar un sistema de migraciones como Alembic
    safe_create_db_and_tables()

app.include_router(api_router, prefix="/api/v1")

@app.get("/")
def read_root():
    return {"message": "Bienvenido al API del Sistema Bancario"}