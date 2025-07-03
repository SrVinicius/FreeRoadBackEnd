from freeroad.domain.repositories.week_repository import WeekRepository
from freeroad.domain.entities.week import Week
from typing import List


class GetAllWeeksUseCase:
    def __init__(self, repository: WeekRepository):
        self.repository = repository

    def execute(self) -> List[Week]:
        """
        Obtém todos os registros de abastecimento.
        
        Returns:
            List[Week]: Lista de todos os registros de abastecimento
        """
        return self.repository.get_all()
