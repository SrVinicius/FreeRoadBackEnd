from fastapi import FastAPI
from freeroad.api.routes import user_route, week_route
from freeroad.api.openapi_tags import openapi_tags
from freeroad.infra.repositories.in_memory_user_repository import InMemoryUserRepository
from freeroad.api.deps import get_user_repository


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


app.include_router(user_route.router, prefix="/users", tags=["Users"])
app.include_router(week_route.router, prefix="/weeks", tags=["Weeks"])

# export PYTHONPATH=/home/devuser/app
