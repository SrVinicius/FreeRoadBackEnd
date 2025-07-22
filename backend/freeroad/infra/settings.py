from dotenv import load_dotenv
import os
import sys

load_dotenv()

DOCKER_ENV = os.getenv("DOCKER_ENV", "0") == "1"

# Configuração para banco de dados local (usando Docker)
POSTGRES_USER = os.getenv("POSTGRES_USER", "bloguser")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "blogpass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "blogdb")
POSTGRES_HOST = "db" if DOCKER_ENV else "localhost"
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# URL do banco de dados - Prioritiza a URL do Neon.tech, se não estiver definida usa local
raw_database_url = os.getenv("DATABASE_URL", None)

# Fallback para URL fixa do Neon se a variável estiver vazia
if not raw_database_url:
    print("AVISO: Variável DATABASE_URL não está definida! Usando URL de fallback.", file=sys.stderr)
    raw_database_url = "postgresql+asyncpg://neondb_owner:npg_VokYPan08Kzl@ep-square-bar-aci9cisu-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require"

# Log para debug (ocultando credenciais)
if '@' in raw_database_url:
    scheme = raw_database_url.split('@')[0].split('://')[0]
    remainder = raw_database_url.split('@')[1]
    print(f"Usando DATABASE_URL: {scheme}://*****@{remainder}", file=sys.stderr)
else:
    print(f"Formato de DATABASE_URL inválido: {raw_database_url[:10]}...", file=sys.stderr)

# Certifique-se de que a URL tem o formato correto
if '://' not in raw_database_url:
    print("AVISO: URL do banco de dados não tem o formato correto, adicionando prefixo.", file=sys.stderr)
    raw_database_url = f"postgresql+asyncpg://{raw_database_url}"

# Formato final da URL
DATABASE_URL = raw_database_url

# Fallback para configuração local se a URL ainda estiver vazia
if DATABASE_URL is None or DATABASE_URL == "":
    print("AVISO: Usando configuração local do banco.", file=sys.stderr)
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
