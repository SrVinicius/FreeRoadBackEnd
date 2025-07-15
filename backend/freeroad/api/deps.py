from fastapi import Depends
from sqlalchemy.orm import Session
from freeroad.infra.database import SessionLocal
from freeroad.infra.repositories.sqlalchemy_week_repository import SQLAlchemyWeekRepository
from freeroad.infra.repositories.in_memory_user_repository import InMemoryUserRepository
from freeroad.infra.repositories.in_memory_week_repository import InMemoryWeekRepository


# Instâncias em memória para simulação
user_repo = InMemoryUserRepository()
week_repo = InMemoryWeekRepository()

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Função para obter o repositório de Week com injeção de dependência
def get_week_repository():
    return week_repo

# Use o repositório SQLAlchemy se precisar dele
def get_sqlalchemy_week_repository(db: Session = Depends(get_db)):
    return SQLAlchemyWeekRepository(session=db)

# Faça o mesmo para outros repositórios, se necessário

# Function to get the user repository
def get_user_repository():
    return user_repo