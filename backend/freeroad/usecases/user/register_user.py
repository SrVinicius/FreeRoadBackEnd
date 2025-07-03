from freeroad.domain.entities.user import User
from freeroad.domain.repositories.user_repository import UserRepository
from typing import Optional


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    def execute(self, user: User) -> Optional[User]:
        return self.repository.register(user)
