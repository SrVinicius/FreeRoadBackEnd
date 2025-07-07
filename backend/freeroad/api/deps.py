from freeroad.infra.repositories.in_memory_user_repository import InMemoryUserRepository
from freeroad.infra.repositories.sqlalchemy_week_repository import SQLAlchemyWeekRepository

# Instâncias em memória para simulação
user_repo = InMemoryUserRepository()
week_repo = SQLAlchemyWeekRepository()

