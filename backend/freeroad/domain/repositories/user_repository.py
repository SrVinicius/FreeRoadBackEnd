from abc import ABC, abstractmethod
from freeroad.domain.entities.user import User
from freeroad.domain.value_objects.email_vo import Email
from freeroad.domain.value_objects.password import Password
from typing import Optional


class UserRepository(ABC):
    @abstractmethod
    def login(self, email: Email, password: Password) -> Optional[User]: ...

    @abstractmethod
    def register(self, user: User) -> User: ...

    @abstractmethod
    def logout(self) -> None: ...

    @abstractmethod
    def get_current_user(self) -> User | None: ...

    @abstractmethod
    def set_current_user(self, user: User) -> None: ...
