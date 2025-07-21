# tests/conftest.py

import os
import pytest_asyncio
from httpx import AsyncClient, ASGITransport
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from freeroad.infra.database import Base
from freeroad.api.main import app
from freeroad.api import deps
from asgi_lifespan import LifespanManager

# URL para o banco de testes (deve bater com seu docker-compose)
TEST_DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+asyncpg://bloguser:blogpass@db:5432/blogdb",
)


@pytest_asyncio.fixture(scope="session")
def event_loop():
    """Evita conflito de loops no pytest-asyncio."""
    import asyncio

    loop = asyncio.new_event_loop()
    yield loop
    loop.close()


@pytest_asyncio.fixture(scope="function")
async def setup_engine():
    """Cria engine e sessão de teste."""
    engine = create_async_engine(TEST_DATABASE_URL, echo=True)
    async_session = async_sessionmaker(
        bind=engine, class_=AsyncSession, expire_on_commit=False
    )

    # Criação de tabelas
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    yield engine, async_session

    # Teardown: drop tables
    # async with engine.begin() as conn:
    #     await conn.run_sync(Base.metadata.drop_all)


@pytest_asyncio.fixture
async def db_session(setup_engine):
    """Cria uma sessão de banco por teste."""
    _, async_session = setup_engine
    async with async_session() as session:
        yield session


@pytest_asyncio.fixture
async def client(setup_engine):
    """Cria cliente de teste com override de dependências."""
    _, async_session = setup_engine

    async def override_get_db():
        async with async_session() as session:
            yield session

    app.dependency_overrides[deps.get_db] = override_get_db

    async with LifespanManager(app):
        transport = ASGITransport(app=app)
        async with AsyncClient(transport=transport, base_url="http://test") as ac:
            yield ac

    app.dependency_overrides.clear()


@pytest_asyncio.fixture
async def user_repository(db_session):
    """Fornece um repositório SQLAlchemy de usuário para testes."""
    from freeroad.infra.repositories.sqlalchemy.sqlalchemy_user_repository import SQLAlchemyUserRepository
    return SQLAlchemyUserRepository(session=db_session)


@pytest_asyncio.fixture
async def week_repository(db_session):
    """Fornece um repositório SQLAlchemy de semana para testes."""
    from freeroad.infra.repositories.sqlalchemy.sqlalchemy_week_repository import SQLAlchemyWeekRepository
    return SQLAlchemyWeekRepository(session=db_session)


@pytest_asyncio.fixture
async def test_user(user_repository):
    """Cria um usuário de teste para uso nos testes."""
    from freeroad.domain.entities.user import User
    from freeroad.domain.value_objects.email_vo import Email
    from freeroad.domain.value_objects.password import Password
    import uuid
    
    user = User(
        id=str(uuid.uuid4()),
        name="Test User",
        email=Email("usuario@teste.com.br"),
        password=Password("testePass@123"),
        role="user"
    )
    
    # Verificar se o usuário já existe
    existing = await user_repository.get_by_email(Email("usuario@teste.com.br"))
    if not existing:
        await user_repository.add(user)
    else:
        user = existing
        
    return user


@pytest_asyncio.fixture
async def authenticated_client(client, test_user):
    """Cliente com autenticação pronta para testes de rotas protegidas."""
    # Fazer login e obter token
    response = await client.post("/login", json={
        "email": "usuario@teste.com.br",
        "password": "testePass@123"
    })
    token = response.json().get("access_token")
    
    # Configurar headers com autenticação
    client.headers.update({"Authorization": f"Bearer {token}"})
    return client