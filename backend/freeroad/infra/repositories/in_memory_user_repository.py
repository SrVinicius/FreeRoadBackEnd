from freeroad.domain.repositories.user_repository import UserRepository
from freeroad.domain.entities.user import User
from freeroad.domain.value_objects.email_vo import Email
from freeroad.domain.value_objects.password import Password
from typing import Optional


class InMemoryUserRepository(UserRepository):
    def __init__(self):
        self.users = {}
        self.current_user = None

    async def register(self, user: User):
        self.users[user.id] = user

    async def get_current_user(self):
        return self.current_user

    async def login(self, email: Email, password: Password):
        for user in self.users.values():
            if user.email == email and user.password == password:
                self.current_user = user
                return user
        return None

    async def set_current_user(self, user: Optional[User]) -> None:
        self.current_user = user

    async def get_by_email(self, email: Email) -> Optional[User]:
        """
        Busca um usuário pelo email.

        Args:
            email (Email): O email do usuário a ser buscado.

        Returns:
            Optional[User]: O usuário encontrado ou None se não existir.
        """
        print(f"Searching for email: {email.value}")  # Log para verificar o email recebido
        print(f"Stored users: {self.users}")  # Log para verificar os usuários armazenados
        for user in self.users.values():
            print(f"Checking user: {user.email.value}")  # Log para verificar cada usuário
            if user.email == email:
                print(f"User found: {user}")  # Log para verificar o usuário encontrado
                return user
        print("No user found")  # Log para indicar que nenhum usuário foi encontrado
        return None
