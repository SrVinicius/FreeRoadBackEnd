from typing import List, Optional, Dict
from uuid import uuid4
from freeroad.domain.entities.week import Week
from freeroad.domain.repositories.week_repository import WeekRepository

class InMemoryWeekRepository(WeekRepository):
    def __init__(self):
        self.weeks: Dict[str, Week] = {}
    
    def get_all(self) -> List[Week]:
        return list(self.weeks.values())
        
    def get_by_id(self, week_id: str) -> Optional[Week]:
        return self.weeks.get(week_id)
        
    def get_by_user_id(self, user_id: str) -> List[Week]:
        return [week for week in self.weeks.values() if week.user_id == user_id]
    
    def create(self, week: Week) -> Optional[Week]:
        if not week.id:
            week.id = str(uuid4())
        self.weeks[week.id] = week
        return week
    
    def delete(self, week_id: str) -> None:
        if week_id in self.weeks:
            del self.weeks[week_id]
    
    def add_final_km(self, week_id: str, final_km: float) -> Optional[Week]:
        week = self.get_by_id(week_id)
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
    
    def calculate_average_efficiency(self, user_id: str) -> Optional[float]:
        user_weeks = self.get_by_user_id(user_id)
        
        # Filtrando weeks que têm eficiência calculada
        weeks_with_efficiency = [week for week in user_weeks if week.eficiencia]
        
        if not weeks_with_efficiency:
            return None
        
        # Calculando média
        total = sum(float(week.eficiencia) for week in weeks_with_efficiency)
        return round(total / len(weeks_with_efficiency), 2)