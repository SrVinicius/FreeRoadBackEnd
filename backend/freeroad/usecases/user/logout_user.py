from freeroad.domain.repositories.user_repository import UserRepository


class LogoutUserUseCase:
    def __init__(self, repository: UserRepository):
        self.repository = repository

    async def execute(self) -> None:
        """
        Realiza o logout do usuário atual, definindo o usuário atual como None.
        """
        await self.repository.set_current_user(None)
