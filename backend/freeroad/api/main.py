from fastapi.middleware.cors import CORSMiddleware
from fastapi import FastAPI, HTTPException
from freeroad.api.routes import user_route, week_route
from freeroad.api.openapi_tags import openapi_tags
from freeroad.infra.repositories.in_memory_user_repository import InMemoryUserRepository
from freeroad.api.deps import get_user_repository
import os
import sys
from urllib.parse import urlparse, ParseResult
from typing import Union, List, Optional


app = FastAPI(
    title="FreeRoad API",  # Atualizar para o nome correto
    description="API de controle de combustível com Clean Architecture, FastAPI e PostgreSQL",
    version="1.0.0",
    contact={"name": "Seu Nome", "email": "viniciusferreirarosario5@gmail.com"},
    license_info={"name": "MIT", "url": "https://opensource.org/licenses/MIT"},
    openapi_tags=openapi_tags,
    redirect_slashes=True,
)

# Configurando o repositório em memória
# user_repository = InMemoryUserRepository()

# def get_user_repository_override():
#     return user_repository

# app.dependency_overrides[get_user_repository] = get_user_repository_override


@app.get("/")
def ola():
    return {"olá": "fastapi"}


# Endpoint de diagnóstico para ajudar na depuração
@app.get("/debug/env", tags=["Debug"])
async def debug_environment():
    """Endpoint temporário para depuração do ambiente (remover em produção)"""
    database_url = os.environ.get("DATABASE_URL", "Não definida")
    
    # Ocultar credenciais para o log
    if '@' in database_url:
        scheme = database_url.split('@')[0].split('://')[0]
        remainder = database_url.split('@')[1]
        safe_url = f"{scheme}://*****@{remainder}"
    else:
        safe_url = "URL_INVÁLIDA"
    
    parsed: Union[ParseResult, str, None] = None
    try:
        parsed = urlparse(database_url)
    except Exception as e:
        parsed = f"Erro ao analisar: {str(e)}"
    
    return {
        "ambiente": os.environ.get("ENV", "Não definido"),
        "database_url_segura": safe_url,
        "database_url_parseada": str(parsed) if parsed else "Erro de parsing",
        "banco_driver": os.environ.get("DATABASE_DRIVER", "Não definido"),
        "python_version": sys.version,
        "sistema_operacional": os.name,
        "variáveis_ambiente": [k for k in os.environ.keys() if k.startswith("DATABASE") or k in ["ENV", "PORT", "HOST"]],
    }


# Configuração do CORS - Importante: isso deve vir ANTES da inclusão dos routers
# para garantir que os cabeçalhos CORS sejam aplicados a todas as rotas
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permite todas as origens (use apenas em desenvolvimento)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]  # Expõe todos os cabeçalhos na resposta
)

app.include_router(user_route.router, prefix="/users", tags=["Users"])
app.include_router(week_route.router, prefix="/weeks", tags=["Weeks"])

# Configuração original do CORS (mantida como comentário para referência)
# origins = [
#     "http://localhost",  # Permitir localhost para desenvolvimento
#     "http://localhost:3000",  # Exemplo de frontend local
#     "http://localhost:5173",  # Vite/Vue/React dev server
#     "https://free-road.vercel.app",  # Adicione o domínio do seu frontend
# ]

# export PYTHONPATH=/home/devuser/app
