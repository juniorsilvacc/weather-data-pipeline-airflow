from src.extract.extract_data import extract_weather_data
from src.transform.transform_data import transform_data
from src.load.load_data import load_weather_data
from dotenv import load_dotenv
from pathlib import Path
import os

env_path = Path(__file__).resolve().parent.parent / ".env"
load_dotenv(env_path)

api_key = os.getenv("API_KEY")
url = f'https://api.openweathermap.org/data/2.5/weather?q=Paraiba,BR&units=metric&appid={api_key}'

def main():
    try:
        print("🚀 Iniciando pipeline...")
        
        # EXTRACT
        bronze = extract_weather_data(url)
        print("✅ Dados extraídos!")
        
        # TRANSFORM
        silver = transform_data()
        print("✅ Dados transformados!")
        
        # LOAD
        load_weather_data("weather_data", silver)

        print("🎯 Pipeline finalizado com sucesso!")

    except Exception as e:
        print(f"❌ Erro na execução: {e}")


if __name__ == "__main__":
    main()
