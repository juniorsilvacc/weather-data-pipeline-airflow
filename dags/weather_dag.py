from datetime import datetime, timedelta
from airflow.decorators import dag, task
from pathlib import Path
import sys
import os

sys.path.insert(0, '/opt/airflow')

from src.extract.extract_data import extract_weather_data
from src.transform.transform_data import transform_data
from src.load.load_data import load_weather_data
from dotenv import load_dotenv

env_path = Path(__file__).resolve().parent.parent / 'config' / '.env'
load_dotenv(env_path)

@dag(
    dag_id='pipeline_weather_etl',
    default_args={
        'owner': 'airflow',
        'depends_on_past': False,
        'retries': 2,
        'retry_delay': timedelta(minutes=5)
    },
    description='Pipeline ETL - Clima PB',
    schedule='0 */1 * * *',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['weather', 'etl']
)
def weather_pipeline():
    
    api_key = os.getenv("API_KEY")
    url = f'https://api.openweathermap.org/data/2.5/weather?q=Paraiba,BR&units=metric&appid={api_key}'
    
    @task
    def extract():
        extract_weather_data(url)
        
    @task
    def transform():
        df = transform_data()
        df.to_parquet('/opt/airflow/data/silver/temp_data.parquet', index=False)
        
    @task 
    def load():
        import pandas as pd
        df = pd.read_parquet('/opt/airflow/data/silver/temp_data.parquet')
        load_weather_data('pb_weather', df)
        
    extract() >> transform() >> load()

weather_pipeline()