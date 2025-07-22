# env.py
import os
from logging.config import fileConfig
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from sqlalchemy import engine_from_config
from sqlalchemy import pool
from sqlalchemy import create_engine
from sqlalchemy.ext.asyncio import create_async_engine

from alembic import context
from dotenv import load_dotenv
load_dotenv()

from freeroad.infra.database import Base
from freeroad.infra.models.user_model import UserModel
from freeroad.infra.models.week_model import WeekModel

# Função para remover parâmetros SSL da URL e colocá-los em connect_args
def parse_db_url(url):
    """
    Parse a database URL and extract SSL parameters for proper use with database drivers.
    
    For asyncpg, SSL parameters should not be passed as query params in URL,
    but through the connect_args dict instead.
    """
    parsed = urlparse(url)
    query_dict = parse_qs(parsed.query)
    
    # Extract SSL-related parameters
    connect_args = {}
    ssl_params = ['sslmode', 'channel_binding']
    
    # Clean query parameters, removing SSL-related ones
    clean_query = {k: v for k, v in query_dict.items() if k not in ssl_params}
    
    # Set SSL flag if needed
    if 'sslmode' in query_dict and query_dict['sslmode'][0] == 'require':
        connect_args['ssl'] = True
        # For psycopg/psycopg2 keep sslmode
        connect_args['sslmode'] = 'require'
    
    # Rebuild cleaned URL
    clean_query_str = urlencode(clean_query, doseq=True)
    clean_url = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, 
         parsed.params, clean_query_str, parsed.fragment)
    )
    
    return clean_url, connect_args

config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)

target_metadata = Base.metadata

def run_migrations_offline() -> None:
    raw_url = os.environ.get("DATABASE_URL_ALEMBIC", 'postgresql://neondb_owner:npg_VokYPan08Kzl@ep-square-bar-aci9cisu-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require')
    if raw_url is None:
        raise Exception("A variável de ambiente 'DATABASE_URL_ALEMBIC' não foi definida.")
    
    url, _ = parse_db_url(raw_url)
    
    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
    )
    with context.begin_transaction():
        context.run_migrations()

def run_migrations_online() -> None:
    raw_url = os.environ.get("DATABASE_URL_ALEMBIC", 'postgresql://neondb_owner:npg_VokYPan08Kzl@ep-square-bar-aci9cisu-pooler.sa-east-1.aws.neon.tech/neondb?sslmode=require')
    if raw_url is None:
        raise Exception("A variável de ambiente 'DATABASE_URL_ALEMBIC' não foi definida.")

    # Parse URL and get connect_args
    url, connect_args = parse_db_url(raw_url)
    
    # Use a engine síncrona para Alembic    
    connectable = create_engine(
        url,
        echo=True,
        connect_args=connect_args
    )

    # Connect usando o engine síncrono
    with connectable.connect() as connection:
        context.configure(
            connection=connection,
            target_metadata=target_metadata,
        )
        with context.begin_transaction():
            context.run_migrations()

if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()
