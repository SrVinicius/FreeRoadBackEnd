from fastapi import Depends
from sqlalchemy.orm import Session
from freeroad.infra.database import SessionLocal
from freeroad.infra.repositories.sqlalchemy_week_repository import SQLAlchemyWeekRepository
from freeroad.infra.repositories.in_memory_user_repository import InMemoryUserRepository

# Instâncias em memória para simulação
user_repo = InMemoryUserRepository()

# Função para obter uma sessão do banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Crie uma função para obter o repositório
def get_week_repository(db: Session = Depends(get_db)):
    return SQLAlchemyWeekRepository(session=db)

# Faça o mesmo para outros repositórios

