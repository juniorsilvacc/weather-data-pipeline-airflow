# 🌦️ Weather Data Pipeline ETL

Este projeto é um pipeline de dados ponta a ponta (End-to-End) que automatiza a coleta, transformação e carga de dados meteorológicos mundiais utilizando a API do OpenWeather. O objetivo principal é criar uma base histórica confiável de clima para futuras análises de tendências e correlações ambientais.

## 🚀 Objetivo do Projeto

Construir um pipeline ETL:

- Coletar dados da API Open Weather
- Tratar, padronizar e enriquecer os dados
- Armazenar os dados persistindo em um banco de dados postgreSQL
- Deixar os dados disponíveis e utilizáveis

## 📐 Arquitetura
<img width="1609" height="872" alt="Image" src="https://github.com/user-attachments/assets/d940f01f-04f8-4edb-97d3-236dc06cd6d1" />

## 🔄 Pipeline ETL

- Extract (Extração): Consumo de dados brutos em formato JSON via OpenWeather API.
- Transform (Transformação): Tratamento e padronização dos dados.
- Load (Carga): Inserção dos dados processados em tabelas normalizadas no PostgreSQL.

## 💎 Padrão de Design de Dados

### `O projeto segue o padrão Medallion Architecture`

### Bronze 🥉
- Dados brutos
- Sem perda de informação
- Formato JSON
- Estrutura próxima à origem

### Silver 🥈
- Dados tratados e padronizados
- Aplicação de regras de negócio
- Formato Parquet

### Gold 🥇
- Dados prontos para análise
- Dashboards e KPIs

## 📂 Estrutura do Projeto

```text
weather-data-pipeline-airflow/
├── config/                                  # Configurações de ambiente e conexões
│   └── airflow.cfg                          # Parâmetros globais do pipeline
│
├── dags/                                    # Orquestração do Airflow
│   └── weather_pipeline_dag.py              # Definição do fluxo de trabalho (DAG)
│
├── data/                                    # Camadas de dados (Lake Local)
│   ├── bronze/                              # Dados brutos extraídos da API
│   ├── silver/                              # Dados limpos e convertidos
│   └── gold/                                # Dados agregados para consumo
│
├── docs/                                    # Documentação do projeto e da API
│   └── setup.md                             # Instruções de configuração
│
├── logs/                                    # Registros de execução do Airflow
│   └── dag_processor/                       # Logs específicos do processamento
│
├── notebooks/                               # Prototipagem e análise exploratória
│   └── weather_analysis.ipynb               # Testes de extração e visualização
│
├── src/                                     # Código fonte (Core da aplicação)
│   ├── config/                              # Configuração do banco de dados
│   ├── extract/                             # Coleta e salva na Bronze
│   ├── transform/                           # Limpa, Transforma e Organiza e salva na Silver
│   ├── load/                                # Persistência final na Gold (Postgres)
│   └── main.py/                             # Ponto de partida
│
├── .env-exemple                             # Modelo para variáveis de ambiente
├── .gitignore                               # Arquivos e pastas ignorados pelo Git
├── README.md                                # Documentação principal
├── docker-compose.yaml                      # Orquestração dos serviços (Airflow/DB)
└── requirements.txt                         # Dependências Python (Airflow, Pandas, etc)
```

## 🛠️ Tecnologias Utilizadas
- Linguagem: **Python 3.x**
- Orquestração: **Apache Airflow (DAGs)**
- Banco de Dados: **PostgreSQL**
- Bibliotecas Principais:
    - requests
    - pandas
    - python-dotenv
    - psycopg2
    - sqlalchemy

## ▶️ Como Executar o Projeto
**Pré-requisitos:**
`Docker & Docker Compose (Recomendado para Airflow)`
`Chave de API da OpenWeatherMap`

### 🐳 Ambiente Docker (RECOMENDADO)

Comandos Principais:

```bash
# 1. Primeira execução ou após mudanças no código/dependências
# (Constrói a imagem e sobe os containers)
docker compose up --build

# 3. Parar os containers mantendo os dados do banco
docker compose stop
```

### 🐍 Ambiente Local
```bash
# Criar o ambiente
python3 -m venv venv

# Ativar o ambiente
source venv/bin/activate

# Instalação das bibliotecas
pip install -r requirements.txt

# Executa o main.py
python3 src/main.py
```

👨‍💻 Autor

Projeto desenvolvido por Junior Silva
