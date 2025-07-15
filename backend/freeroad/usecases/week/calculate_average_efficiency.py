from freeroad.domain.repositories.week_repository import WeekRepository
from typing import Optional


class CalculateAverageEfficiencyUseCase:
    def __init__(self, repo):
        self.repo = repo

    async def execute(self, user_id: str) -> float:
        return await self.repo.calculate_average_efficiency(user_id)
