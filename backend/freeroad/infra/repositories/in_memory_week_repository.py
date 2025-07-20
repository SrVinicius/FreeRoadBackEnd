from typing import List, Optional, Dict
from uuid import uuid4
from freeroad.domain.entities.week import Week
from freeroad.domain.repositories.week_repository import WeekRepository

class InMemoryWeekRepository(WeekRepository):
    def __init__(self):
        self.weeks: Dict[str, Week] = {}

    async def get_all(self) -> List[Week]:
        return list(self.weeks.values())

    async def get_by_id(self, week_id: str) -> Optional[Week]:
        return self.weeks.get(week_id)

    async def get_by_user_id(self, user_id: str) -> List[Week]:
        return [week for week in self.weeks.values() if week.user_id == user_id]

    async def create(self, week: Week) -> Optional[Week]:
        if not week.id:
            week.id = str(uuid4())
        self.weeks[week.id] = week
        return week

    async def delete(self, week_id: str) -> None:
        if week_id in self.weeks:
            del self.weeks[week_id]

    async def add_final_km(self, week_id: str, final_km: float) -> Optional[Week]:
        week = await self.get_by_id(week_id)
        if not week:
            return None

        # Convertendo para float para cálculos
        km_atual = float(week.kmAtual)
        litros = float(week.litrosAbastecidos)

        # Atualizando valores
        week.kmFinal = str(final_km)

        # Calculando eficiência se possível
        if litros > 0:
            distancia = final_km - km_atual
            eficiencia = distancia / litros
            week.eficiencia = str(round(eficiencia, 2))

        return week