import pandas as pd
from pathlib import Path
import json
import logging

# -- Etapas --
# ✅ Normalização
# ✅ Rename
# ✅ Drop de colunas
# ✅ Conversão de datetime
# ✅ Enforce de tipos
# ✅ Tratamento de nulos
# ✅ Deduplicação
# ✅ Colunas derivadas
# ✅ Validação de schema
# ✅ Logs mais informativos

# ==========================
# CONFIGURAÇÕES
# ==========================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

FILE_PATH = Path("data/bronze/weather_data_raw.json")
SILVER_PATH = Path("data/silver/weather_data.parquet")

# Colunas que serão dropadas, após tratamento
COLUMNS_TO_DROP = ["weather", "weather_icon", "sys.type"]

# Mapeamento para renomear colunas
COLUMNS_TO_RENAME = {   
    "base": "base",
    "visibility": "visibility",
    "dt": "datetime",
    "timezone": "timezone",
    "id": "city_id", 
    "name": "city_name",
    "cod": "code",
    "coord.lon": "longitude",
    "coord.lat": "latitude",
    "main.temp": "temperature",
    "main.feels_like": "feels_like",
    "main.temp_min": "temp_min",
    "main.temp_max": "temp_max",
    "main.pressure": "pressure",
    "main.humidity": "humidity",
    "main.sea_level": "sea_level",
    "main.grnd_level": "grnd_level",
    "wind.speed": "wind_speed",
    "wind.deg": "wind_deg",
    "wind.gust": "wind_gust",
    "clouds.all": "clouds", 
    "sys.type": "sys_type",                 
    "sys.id": "sys_id",                
    "sys.country": "country",                
    "sys.sunrise": "sunrise",                
    "sys.sunset": "sunset",
}

# Colunas que são timestamps Unix e precisam virar datetime
DATETIME_COLUMNS = ["datetime", "sunrise", "sunset"]

# Colunas obrigatórias para validação
REQUIRED_COLUMNS = ["temperature", "humidity", "datetime", "city_id"]

# Tipos esperados para otimização e padronização
DTYPE_MAP = {
    "temperature": "float32",
    "feels_like": "float32",
    "temp_min": "float32",
    "temp_max": "float32",
    "humidity": "int16",
    "pressure": "int32",
    "clouds": "int16",
    "wind_speed": "float32",
    "wind_gust": "float32",
    "visibility": "int32",
}

def create_dataframe(path: Path) -> pd.DataFrame:
    """
    Lê o arquivo JSON da camada Bronze e transforma em um DataFrame.
    """
    logging.info("Lendo arquivo JSON...")

    if not path.exists():
        raise FileNotFoundError(f"Arquivo não encontrado: {path}")

    with open(path, encoding="utf-8") as file:
        data = json.load(file)

    # Converte JSON aninhado em colunas planas
    df = pd.json_normalize(data)

    logging.info(f"DataFrame criado com {len(df)} linha(s)")
    return df

def normalize_weather(df: pd.DataFrame) -> pd.DataFrame:
    """
    A coluna 'weather' vem como lista de dicionários. Aqui extraímos as informações e transformamos em colunas.
    """
    if "weather" not in df.columns:
        return df

    # Pega o primeiro item da lista weather
    weather_df = pd.json_normalize(df["weather"].str[0])

    # Renomeia colunas para evitar conflito
    weather_df = weather_df.rename(columns={
        "id": "weather_id",
        "main": "weather_main",
        "description": "weather_description",
        "icon": "weather_icon",
    })

    # Junta com DataFrame original
    df = pd.concat([df, weather_df], axis=1)

    logging.info("Coluna 'weather' normalizada")
    return df

def drop_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove colunas que não serão utilizadas.
    """
    existing = [col for col in COLUMNS_TO_DROP if col in df.columns]
    df = df.drop(columns=existing)

    logging.info(f"Colunas removidas: {existing}")
    return df

def rename_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Padroniza nomes das colunas.
    """
    df = df.rename(columns=COLUMNS_TO_RENAME)
    logging.info("Colunas renomeadas")
    return df

def convert_datetime(df: pd.DataFrame) -> pd.DataFrame:
    """
    Converte colunas Unix timestamp para datetime e ajusta para o fuso horário do Brasil.
    """
    for col in DATETIME_COLUMNS:
        if col in df.columns:
            df[col] = (
                pd.to_datetime(df[col], unit="s", utc=True)
                .dt.tz_convert("America/Sao_Paulo")
            )

    logging.info("Colunas datetime convertidas")
    return df

def validate_schema(df: pd.DataFrame):
    """
    Verifica se as colunas obrigatórias existem no DataFrame.
    """
    missing = [col for col in REQUIRED_COLUMNS if col not in df.columns]

    if missing:
        raise ValueError(f"Colunas obrigatórias ausentes: {missing}")

    logging.info("Schema validado com sucesso")

def enforce_dtypes(df: pd.DataFrame) -> pd.DataFrame:
    """
    Aplica tipos de dados padronizados para otimização.
    """
    for col, dtype in DTYPE_MAP.items():
        if col in df.columns:
            df[col] = df[col].astype(dtype)

    logging.info("Tipos de dados aplicados")
    return df

def handle_nulls(df: pd.DataFrame) -> pd.DataFrame:
    """
    Trata valores nulos em colunas específicas.
    """
    if "wind_gust" in df.columns:
        df["wind_gust"] = df["wind_gust"].fillna(0)

    if "sea_level" in df.columns and "pressure" in df.columns:
        df["sea_level"] = df["sea_level"].fillna(df["pressure"])

    logging.info("Tratamento de valores nulos aplicado")
    return df

def create_derived_columns(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cria colunas derivadas para facilitar análises futuras.
    """
    # Converter Kelvin para Celsius (caso API esteja em Kelvin)
    if "temperature" in df.columns:
        df["temperature_c"] = df["temperature"] - 273.15

    # Criar colunas de data e hora
    if "datetime" in df.columns:
        df["date"] = df["datetime"].dt.date
        df["hour"] = df["datetime"].dt.hour

    logging.info("Colunas derivadas criadas")
    return df

def remove_duplicates(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove registros duplicados com base na cidade e datetime.
    """
    if "city_id" in df.columns and "datetime" in df.columns:
        before = len(df)
        df = df.drop_duplicates(subset=["city_id", "datetime"])
        after = len(df)
        logging.info(f"Removidos {before - after} registros duplicados")

    return df

def transform_data() -> pd.DataFrame:
    """
    Executa todas as transformações da camada Bronze para Silver.
    """
    logging.info("🚀 Iniciando transformações...")

    df = create_dataframe(FILE_PATH)
    df = normalize_weather(df)
    df = drop_columns(df)
    df = rename_columns(df)
    df = convert_datetime(df)
    
    validate_schema(df)
    
    df = enforce_dtypes(df)
    df = handle_nulls(df)
    df = create_derived_columns(df)
    df = remove_duplicates(df)

    # Criar pasta silver se não existir
    #SILVER_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Salvar em Parquet
    #df.to_parquet(SILVER_PATH, index=False)

    #logging.info(f"Arquivo Silver salvo em {SILVER_PATH}")
    logging.info("Transformações concluídas ✅")
    return df
