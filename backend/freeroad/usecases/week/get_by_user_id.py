from freeroad.domain.repositories.week_repository import WeekRepository
from freeroad.domain.entities.week import Week
from typing import List


class GetWeeksByUserIdUseCase:
    def __init__(self, repository: WeekRepository):
        self.repository = repository

    async def execute(self, user_id: str) -> List[Week]:
        """
        Obtém todos os registros de abastecimento de um usuário específico.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            List[Week]: Lista de registros de abastecimento do usuário
        """
        return await self.repository.get_by_user_id(user_id)
