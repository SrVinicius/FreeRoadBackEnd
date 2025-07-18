from freeroad.domain.repositories.week_repository import WeekRepository
from freeroad.domain.entities.week import Week
from typing import Optional


class GetWeekByIdUseCase:
    def __init__(self, repository: WeekRepository):
        self.repository = repository

    async def execute(self, week_id: str) -> Optional[Week]:
        """
        Obtém um registro de abastecimento pelo ID.
        
        Args:
            week_id: ID do registro a ser obtido
            
        Returns:
            Week: O objeto Week correspondente, ou None se não encontrado
        """
        return await self.repository.get_by_id(week_id)
