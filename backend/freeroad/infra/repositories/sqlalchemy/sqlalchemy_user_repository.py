from typing import Optional, List, cast
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from uuid import uuid4

from freeroad.domain.repositories.user_repository import UserRepository
from freeroad.domain.entities.user import User
from freeroad.domain.value_objects.email_vo import Email
from freeroad.domain.value_objects.password import Password
from freeroad.infra.models.user_model import UserModel


class SQLAlchemyUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session
        self.current_user: Optional[User] = None  # Use Optional[User] for type compatibility

    async def register(self, user: User) -> User:
        """
        Registra um novo usuário no banco de dados.

        Args:
            user (User): O usuário a ser registrado.

        Returns:
            User: O usuário registrado.
        """
        if not user.id:
            user.id = str(uuid4())
            
        user_model = UserModel(
            id=user.id,
            name=user.name,
            email=str(user.email.value),
            password=str(user.password.value),
            role=user.role
        )
        
        self.session.add(user_model)
        await self.session.commit()
        await self.session.refresh(user_model)
        
        return user_model.to_entity()

    async def get_current_user(self) -> Optional[User]:
        """
        Retorna o usuário atual.

        Returns:
            Optional[User]: O usuário atual ou None.
        """
        return self.current_user

    async def login(self, email: Email, password: Password) -> Optional[User]:
        """
        Autentica um usuário com base no email e senha.

        Args:
            email (Email): O email do usuário.
            password (Password): A senha do usuário.

        Returns:
            Optional[User]: O usuário autenticado ou None.
        """
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == str(email.value))
        )
        user_model = result.scalar_one_or_none()
        
        password_str = str(cast(Password, password).value)

        if user_model and password_str == user_model.password:
            user = user_model.to_entity()
            self.current_user = user
            return user
            
        return None

    async def set_current_user(self, user: Optional[User]) -> None:
        """
        Define o usuário atual.

        Args:
            user (Optional[User]): O usuário a ser definido como atual ou None para logout.
        """
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
        result = await self.session.execute(
            select(UserModel).where(UserModel.email == str(email.value))
        )
        user_model = result.scalar_one_or_none()
        print(f"UserModel found: {user_model}")  # Log para verificar o resultado da consulta
        return user_model.to_entity() if user_model else None
    
    async def get_by_id(self, user_id: str) -> Optional[User]:
        """
        Busca um usuário pelo ID.

        Args:
            user_id (str): O ID do usuário a ser buscado.

        Returns:
            Optional[User]: O usuário encontrado ou None se não existir.
        """
        result = await self.session.execute(
            select(UserModel).where(UserModel.id == user_id)
        )
        user_model = result.scalar_one_or_none()
        
        return user_model.to_entity() if user_model else None
    
    async def get_all(self) -> List[User]:
        """
        Retorna todos os usuários.

        Returns:
            List[User]: Lista de todos os usuários.
        """
        result = await self.session.execute(select(UserModel))
        return [user_model.to_entity() for user_model in result.scalars().all()]
    
    async def create(self, user: User) -> User:
        """
        Cria um novo usuário.

        Args:
            user (User): O usuário a ser criado.

        Returns:
            User: O usuário criado.
        """
        return await self.register(user)

    async def add(self, user: User) -> User:
        """
        Adiciona um usuário (alias para register).
        
        Args:
            user (User): O usuário a ser adicionado.
            
        Returns:
            User: O usuário adicionado.
        """
        return await self.register(user)