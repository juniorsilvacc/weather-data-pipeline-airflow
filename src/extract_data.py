import json
import requests
from pathlib import Path
import logging
from typing import Dict

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

def get_data(url: str) -> Dict:
    """Faz requisição HTTP e retorna o JSON da resposta."""
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        logging.info("Requisição realizada com sucesso.")
        return response.json()
    
    except requests.exceptions.RequestException as e:
        logging.error(f"Erro na requisição: {e}")
        return {}
    
def save_to_bronze(data: Dict, output_path: str) -> None:
    """Salva os dados brutos na camada Bronze."""
    if not data:
        logging.warning("Nenhum dado para salvar.")
        return
    
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)

    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

    logging.info(f"Arquivo salvo em {output_path}")

def extract_weather_data(url: str) -> Dict:
    """Orquestra o processo de extração."""
    data = get_data(url)
    save_to_bronze(data, "data/bronze/weather_data.json")
    return data