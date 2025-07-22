from dotenv import load_dotenv
import os

load_dotenv()

DOCKER_ENV = os.getenv("DOCKER_ENV", "0") == "1"

# Configuração para banco de dados local (usando Docker)
POSTGRES_USER = os.getenv("POSTGRES_USER", "bloguser")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD", "blogpass")
POSTGRES_DB = os.getenv("POSTGRES_DB", "blogdb")
POSTGRES_HOST = "db" if DOCKER_ENV else "localhost"
POSTGRES_PORT = os.getenv("POSTGRES_PORT", "5432")

# URL do banco de dados - Prioritiza a URL do Neon.tech, se não estiver definida usa local
DATABASE_URL = os.getenv(
    "DATABASE_URL", 
    "postgresql+asyncpg://neondb_owner:npg_VokYPan08Kzl@ep-square-bar-aci9cisu-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require"
)

# Fallback para configuração local se não houver DATABASE_URL
if DATABASE_URL is None or DATABASE_URL == "":
    DATABASE_URL = f"postgresql+asyncpg://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"
