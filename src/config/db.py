from sqlalchemy import create_engine
from urllib.parse import quote_plus
from pathlib import Path
from dotenv import load_dotenv
import logging
import os

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

# Carregar variáveis de ambiente
env_path = Path(__file__).resolve().parent.parent.parent / ".env"
load_dotenv(env_path)

DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT", 5432)

def get_engine():
    """
    Cria conexão com PostgreSQL usando SQLAlchemy.
    """
    connection_string = (
        f"postgresql+psycopg2://{DB_USER}:"
        f"{quote_plus(DB_PASSWORD)}@"
        f"{DB_HOST}:{DB_PORT}/"
        f"{DB_NAME}"
    )

    logging.info(f"Conectando em {DB_HOST}:{DB_PORT}/{DB_NAME}")

    return create_engine(connection_string)