from freeroad.domain.repositories.week_repository import WeekRepository
from typing import Optional


class CalculateAverageEfficiencyUseCase:
    def __init__(self, repository: WeekRepository):
        self.repository = repository

    def execute(self, user_id: str) -> Optional[float]:
        """
        Calcula a eficiência média de combustível para um usuário específico.
        
        Args:
            user_id: ID do usuário
            
        Returns:
            float: A eficiência média em km/l, ou None se não houver dados suficientes
        """
        return self.repository.calculate_average_efficiency(user_id)
