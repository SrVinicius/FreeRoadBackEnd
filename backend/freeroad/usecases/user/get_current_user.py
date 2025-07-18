from freeroad.domain.repositories.user_repository import UserRepository
from freeroad.domain.entities.user import User
from typing import Optional


class GetCurrentUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self) -> Optional[User]:
        return await self.repository.get_current_user()
