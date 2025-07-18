from freeroad.domain.repositories.week_repository import WeekRepository
from typing import Optional
from freeroad.domain.entities.week import Week


class AddFinalKmUseCase:
    def __init__(self, repository: WeekRepository):
        self.repository = repository

    async def execute(self, week_id: str, final_km: float) -> Optional[Week]:
        """
        Adiciona a quilometragem final a um registro de abastecimento e
        calcula a eficiência com base na distância percorrida e litros abastecidos.
        
        Args:
            week_id: ID do registro a ser atualizado
            final_km: Quilometragem final
            
        Returns:
            Week: O objeto Week atualizado, ou None se não encontrado
        """
        return await self.repository.add_final_km(week_id, final_km)
