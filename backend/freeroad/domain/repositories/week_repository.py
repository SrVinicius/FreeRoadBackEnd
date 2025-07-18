from abc import ABC, abstractmethod
from freeroad.domain.entities.week import Week
from typing import Optional, List


class WeekRepository(ABC):
    @abstractmethod
    async def get_all(self) -> List[Week]: ...

    @abstractmethod
    async def get_by_id(self, week_id: str) -> Optional[Week]: ...

    @abstractmethod
    async def get_by_user_id(self, user_id: str) -> List[Week]: ...
    
    @abstractmethod
    async def create(self, week: Week) -> Optional[Week]: ...

    @abstractmethod
    async def delete(self, week_id: str) -> None: ...
    
    @abstractmethod
    async def add_final_km(self, week_id: str, final_km: float) -> Optional[Week]: ...

    @abstractmethod
    async def calculate_average_efficiency(self, user_id: str) -> Optional[float]: ...
    