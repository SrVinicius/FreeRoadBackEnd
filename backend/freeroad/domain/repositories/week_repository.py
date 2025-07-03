from abc import ABC, abstractmethod
from freeroad.domain.entities.week import Week
from typing import Optional, List


class WeekRepository(ABC):
    @abstractmethod
    def get_all(self) -> List[Week]: ...

    @abstractmethod
    def get_by_id(self, week_id: str) -> Optional[Week]: ...
    
    @abstractmethod
    def get_by_user_id(self, user_id: str) -> List[Week]: ...
    
    @abstractmethod
    def create(self, week: Week) -> Optional[Week]: ...

    @abstractmethod
    def delete(self, week_id: str) -> None: ...
    
    @abstractmethod
    def add_final_km(self, week_id: str, final_km: float) -> Optional[Week]: ...

    @abstractmethod
    def calculate_average_efficiency(self, user_id: str) -> Optional[float]: ...
    