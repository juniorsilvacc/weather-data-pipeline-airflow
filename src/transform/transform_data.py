import pandas as pd
from pathlib import Path
import json
import logging

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

    # Criar pasta silver se não existir
    SILVER_PATH.parent.mkdir(parents=True, exist_ok=True)

    # Salvar em Parquet
    df.to_parquet(SILVER_PATH, index=False)

    logging.info(f"Arquivo Silver salvo em {SILVER_PATH}")
    logging.info("Transformações concluídas ✅")
    return df