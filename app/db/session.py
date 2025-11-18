from sqlmodel import create_engine, Session, SQLModel
from app.core.config import (
    DATABASE_URL,
    DB_HOST,
    DB_USERNAME,
    DB_PASSWORD,
    DB_NAME,
)
import logging

# === DIAGNÓSTICO: IMPRIMIR CONEXIÓN REAL ===
print("====================================================")
print("🔍 DIAGNÓSTICO DE CONEXIÓN A BASE DE DATOS:")
print(f"🔗 DATABASE_URL → {DATABASE_URL}")
print(f"🏠 HOST_DB      → {DB_HOST}")
print(f"👤 USER_DB      → {DB_USERNAME}")
print(f"📦 DB_NAME      → {DB_NAME}")
print("====================================================")

ssl_args = {'ssl': {'ca': 'ca.pem'}}
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- LÓGICA DE CONEXIÓN CONDICIONAL ---

if DB_HOST in ("localhost", "127.0.0.1"):
    logger.info("🔧 Detectado entorno local. Creando engine de base de datos sin SSL.")
    engine = create_engine(DATABASE_URL)
else:
    logger.info("☁️ Detectado entorno de nube/producción. Creando engine con SSL.")
    ssl_args = {'ssl': {'ca': 'ca.pem'}}
    engine = create_engine(DATABASE_URL, connect_args=ssl_args)


def create_db_and_tables():
    pass


def get_session():
    with Session(engine) as session:
        yield session
