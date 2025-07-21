import pytest
import uuid
from freeroad.domain.entities.user import User
from freeroad.domain.value_objects.email_vo import Email
from freeroad.domain.value_objects.password import Password
from freeroad.usecases.user.register_user import RegisterUserUseCase
from freeroad.usecases.user.login_user import LoginUserUseCase
from freeroad.usecases.user.logout_user import LogoutUserUseCase
from freeroad.usecases.user.get_current_user import GetCurrentUserUseCase
from freeroad.usecases.user.set_current_user import SetCurrentUserUseCase


def create_test_user() -> User:
    """Cria um usuário para teste com valores aleatórios"""
    return User(
        id=str(uuid.uuid4()),
        name="Test User",
        email=Email(f"user_{uuid.uuid4()}@test.com"),
        password=Password("StrongPass@123"),
        role="user"
    )


@pytest.mark.asyncio
async def test_register_user_success(user_repository):
    """Testa o caso de uso de registro de usuário com sucesso"""
    # Arrange
    usecase = RegisterUserUseCase(user_repository)
    user = create_test_user()
    
    # Act
    result = await usecase.execute(user)
    
    # Assert
    assert result is not None
    assert result.id == user.id
    assert result.name == user.name
    assert str(result.email.value) == str(user.email.value)
    
    # Verificar se o usuário foi definido como atual após o registro
    current_user = await user_repository.get_current_user()
    assert current_user is not None
    assert current_user.id == user.id
    
    # Verificar se o usuário foi persistido no banco
    db_user = await user_repository.get_by_email(user.email)
    assert db_user is not None
    assert db_user.id == user.id


@pytest.mark.asyncio
async def test_login_user_success(user_repository):
    """Testa o caso de uso de login de usuário com sucesso"""
    # Arrange
    email = Email("login_test@example.com")
    password = Password("LoginTest@123")
    
    user = User(
        id=str(uuid.uuid4()),
        name="Login Test User",
        email=email,
        password=password,
        role="user"
    )
    
    # Registrar o usuário primeiro
    await user_repository.register(user)
    
    # Inicialmente, não há usuário atual
    await user_repository.set_current_user(None)
    assert await user_repository.get_current_user() is None
    
    # Act - Fazer login
    usecase = LoginUserUseCase(user_repository)
    result = await usecase.execute(email, password)
    
    # Assert
    assert result is not None
    assert result.id == user.id
    assert str(result.email.value) == str(email.value)
    
    # Verificar se o usuário foi definido como atual após o login
    current_user = await user_repository.get_current_user()
    assert current_user is not None
    assert current_user.id == user.id


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(user_repository):
    """Testa o caso de uso de login de usuário com credenciais inválidas"""
    # Arrange
    correct_email = Email("invalid_login@example.com")
    correct_password = Password("CorrectPass@123")
    
    user = User(
        id=str(uuid.uuid4()),
        name="Invalid Login Test User",
        email=correct_email,
        password=correct_password,
        role="user"
    )
    
    # Registrar o usuário primeiro
    await user_repository.register(user)
    
    # Limpar usuário atual
    await user_repository.set_current_user(None)
    
    # Act - Tentar login com senha incorreta
    usecase = LoginUserUseCase(user_repository)
    result = await usecase.execute(correct_email, Password("WrongPass@123"))
    
    # Assert
    assert result is None
    
    # Verificar que o usuário atual continua sendo None
    current_user = await user_repository.get_current_user()
    assert current_user is None
    
    # Act - Tentar login com email incorreto
    wrong_email = Email("wrong_email@example.com")
    result = await usecase.execute(wrong_email, correct_password)
    
    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_logout_user(user_repository):
    """Testa o caso de uso de logout de usuário"""
    # Arrange
    user = create_test_user()
    await user_repository.register(user)
    
    # Garantir que há um usuário atual
    await user_repository.set_current_user(user)
    assert await user_repository.get_current_user() is not None
    
    # Act
    usecase = LogoutUserUseCase(user_repository)
    await usecase.execute()
    
    # Assert
    current_user = await user_repository.get_current_user()
    assert current_user is None


@pytest.mark.asyncio
async def test_get_current_user(user_repository):
    """Testa o caso de uso para obter o usuário atual"""
    # Arrange
    user = create_test_user()
    
    # Definir usuário atual
    await user_repository.set_current_user(user)
    
    # Act
    usecase = GetCurrentUserUseCase(user_repository)
    result = await usecase.execute()
    
    # Assert
    assert result is not None
    assert result.id == user.id
    assert str(result.email.value) == str(user.email.value)


@pytest.mark.asyncio
async def test_get_current_user_none(user_repository):
    """Testa o caso de uso para obter o usuário atual quando não há usuário definido"""
    # Arrange
    await user_repository.set_current_user(None)
    
    # Act
    usecase = GetCurrentUserUseCase(user_repository)
    result = await usecase.execute()
    
    # Assert
    assert result is None


@pytest.mark.asyncio
async def test_set_current_user(user_repository):
    """Testa o caso de uso para definir o usuário atual"""
    # Arrange
    user = create_test_user()
    usecase = SetCurrentUserUseCase(user_repository)
    
    # Act
    await usecase.execute(user)
    
    # Assert
    current_user = await user_repository.get_current_user()
    assert current_user is not None
    assert current_user.id == user.id
    assert str(current_user.email.value) == str(user.email.value)
    
    # Definir como None
    await usecase.execute(None)
    assert await user_repository.get_current_user() is None
