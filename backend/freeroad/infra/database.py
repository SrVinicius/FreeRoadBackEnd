from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.orm import declarative_base
import os
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

from freeroad.infra.settings import DATABASE_URL

# Função para remover parâmetros SSL da URL e colocá-los em connect_args
def parse_db_url(url):
    """
    Parse a database URL and extract SSL parameters for proper use with asyncpg.
    
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
    
    # Rebuild cleaned URL
    clean_query_str = urlencode(clean_query, doseq=True)
    clean_url = urlunparse(
        (parsed.scheme, parsed.netloc, parsed.path, 
         parsed.params, clean_query_str, parsed.fragment)
    )
    
    return clean_url, connect_args

if DATABASE_URL is None:
    raise ValueError("DATABASE_URL must be set")

# Parse the URL to properly handle SSL parameters
CLEAN_DATABASE_URL, CONNECT_ARGS = parse_db_url(DATABASE_URL)

engine = create_async_engine(
    CLEAN_DATABASE_URL, 
    echo=True,
    connect_args=CONNECT_ARGS
)

async_session = async_sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)

Base = declarative_base()