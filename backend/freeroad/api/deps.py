from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.ext.asyncio import AsyncSession
# from freeroad.infra.database import SessionLocal
from freeroad.infra.repositories.sqlalchemy.sqlalchemy_week_repository import SQLAlchemyWeekRepository
from freeroad.infra.repositories.in_memory_user_repository import InMemoryUserRepository
from freeroad.infra.repositories.in_memory_week_repository import InMemoryWeekRepository
from typing import Generator


# Instâncias em memória para simulação
user_repo = InMemoryUserRepository()
week_repo = InMemoryWeekRepository()

security = HTTPBearer()

from sqlalchemy.ext.asyncio import AsyncSession
from freeroad.infra.database import async_session
from freeroad.domain.entities.user import User
from collections.abc import AsyncGenerator


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    async with async_session() as session:
        yield session

# Função para obter o repositório de Week com injeção de dependência
def get_week_repository() -> InMemoryWeekRepository:
    return week_repo

# Use o repositório SQLAlchemy se precisar dele
def get_sqlalchemy_week_repository(db: AsyncSession = Depends(get_db)) -> SQLAlchemyWeekRepository:
    return SQLAlchemyWeekRepository(session=db)

# Função para obter o repositório de usuário
def get_user_repository() -> InMemoryUserRepository:
    return user_repo

# Função para obter o usuário atual
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> dict:
    token = credentials.credentials
    user = await user_repo.get_current_user()  # Adicione o await para resolver a coroutine
    if not user or user.id != token:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Usuário não autenticado.")
    return user