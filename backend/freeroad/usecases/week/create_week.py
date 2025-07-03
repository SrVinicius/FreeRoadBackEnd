from freeroad.domain.repositories.week_repository import WeekRepository
from freeroad.domain.entities.week import Week
from typing import Optional


class CreateWeekUseCase:
    def __init__(self, repository: WeekRepository):
        self.repository = repository

    def execute(self, week: Week) -> Optional[Week]:
        """
        Cria um novo registro de abastecimento.
        
        Args:
            week: Objeto Week contendo os dados do abastecimento
            
        Returns:
            Week: O objeto Week criado, ou None se a criação falhar
        """
        return self.repository.create(week)
