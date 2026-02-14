# 🛠️ Setup do Projeto
Este projeto utiliza uma arquitetura de Medallion Lakehouse local e persistência em banco de dados relacional para análise.

## Ambiente de Execução
Utilizamos o `venv` para garantir que as versões das bibliotecas não conflitem com outros projetos.

## Ambiente Local (Manual)
```bash
# Criar o ambiente
python3 -m venv venv

# Ativar o ambiente
source venv/bin/activate

# Instalação das bibliotecas
pip install -r requirements.txt
```

## Ambiente de Docker (Recomendado)

```bash
# Primeira execução. Sobe o banco PostgreSQL e executa o ETL automaticamente
docker compose up --build

# Para rodar em background (detach mode)
docker compose up -d

# Reexecutar o ETL, sem precisar reconstruir tudo
docker start -a <container>
```

## Infraestrutura e Banco de Dados
Verificação do PostgreSQL (WSL/Linux)
Caso opte por rodar o banco fora do Docker, valide o status do serviço:

```bash
    # Abra seu terminal do WSL (Ubuntu por exemplo) e rode:
    psql --version

    # Ver o status do postgresql
    sudo service postgresql status

    # Ativar localmente
    sudo service postgresql start

    # Testar conexão
    sudo -u postgres psql
```

## Variáveis de Ambiente (.env)
Crie um arquivo .env na raiz do projeto e preencha suas credenciais:

```bash
API_KEY=
DB_HOST=localhost # No Docker, use 'db'
DB_NAME=weather_db
DB_USER=postgres
DB_PASSWORD=postgres
DB_PORT=5432
```

## Organização do Data Lake Local
O projeto utiliza o conceito de partições temporais. A estrutura de pastas é gerada automaticamente pelo pipeline:

```text
data/
├── bronze/                                 # Dados brutos (Imutáveis)
│   └── weather_data_raw.json
└── silver/                                 # Dados limpos e tipados
    └── weather_data.parquet
```

## Gestão de Dependências
Para garantir a rastreabilidade das versões, sempre que instalar um pacote novo, atualize o arquivo de requisitos

```bash
pip freeze > requirements.txt
```

### Pacotes Utilizados
- pandas: Manipulação e transformação de dados.
- sqlalchemy: Interface com o banco de dados.
- python-dotenv: Gestão de variáveis de ambiente.
- requests: Consumo de APIs externas.
- pyarrow: Engine para escrita de arquivos Parquet.