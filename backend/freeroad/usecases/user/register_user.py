from freeroad.domain.entities.user import User
from freeroad.domain.repositories.user_repository import UserRepository
from typing import Optional


class RegisterUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self, user: User):
        await self.repository.register(user)
        await self.repository.set_current_user(user)  # Set the current user
        return user
