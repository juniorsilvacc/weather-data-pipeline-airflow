# 🌦️ Weather Data Pipeline ETL

Este projeto é um pipeline de dados ponta a ponta (End-to-End) que automatiza a coleta, transformação e carga de dados meteorológicos mundiais utilizando a API do OpenWeather.
O objetivo principal é criar uma base histórica confiável de clima para futuras análises de tendências e correlações ambientais.

## 🛠️ Tecnologias Utilizadas
- Linguagem: Python 3.x
- Orquestração: Apache Airflow (DAGs)
- Banco de Dados: PostgreSQL
- Bibliotecas Principais: `requests, pandas, python-dotenv, psycopg2, sqlalchemy`

## 🏗️ Arquitetura do Pipeline (ETL)
- Extract (Extração): Consumo de dados brutos em formato JSON via OpenWeather API.
- Transform (Transformação):
- Load (Carga): Inserção dos dados processados em tabelas normalizadas no PostgreSQL.

### `O projeto segue o padrão Medallion Architecture`

### Bronze 🥉
- Dados brutos
- Sem perda de informação
- Formato JSON
- Estrutura próxima à origem

### Silver 🥈
- Dados tratados e padronizados
- Aplicação de regras de negócio
- Cálculo de métricas
- Formato Parquet

### Gold 🥇
- Dados prontos para análise
- Dashboards e KPIs

## 🚀 Como Executar
**Pré-requisitos:**
Docker & Docker Compose (Recomendado para Airflow)
Chave de API da OpenWeatherMap

### Configuração:
```bash
    ...
```
