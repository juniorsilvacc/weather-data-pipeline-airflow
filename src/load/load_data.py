from src.config.db import get_engine
from sqlalchemy import inspect
import pandas as pd
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def load_weather_data(table_name: str, df: pd.DataFrame):
    """
    Insere DataFrame no PostgreSQL. A tabela será criada automaticamente se não existir.
    """
    if df.empty:
        logging.warning("DataFrame vazio. Nada para inserir.")
        return

    try:
        engine = get_engine()
        inspector = inspect(engine)
        
        # Verifica se tabela já existe
        if not inspector.has_table(table_name):
            logging.info("Tabela não existe. Criando tabela...")
            df.head(0).to_sql(
                name=table_name,
                con=engine,
                if_exists="replace",
                index=False
            )
            logging.info("Tabela criada com sucesso!")

        # Inseri os dados
        df.to_sql(
            name=table_name,
            con=engine,
            if_exists="append",  # append, replace ou fail
            index=False,
            method="multi"  # melhora performance
        )

        logging.info("✅ Dados carregados com sucesso!")

    except Exception as e:
        logging.error(f"Erro ao carregar dados: {e}")
        raise