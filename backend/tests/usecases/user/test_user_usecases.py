import uuid
from blog.domain.entities.user import User
from blog.domain.value_objects.email_vo import Email
from blog.domain.value_objects.password import Password
from blog.infra.repositories.in_memory_user_repository import InMemoryUserRepository
from blog.usecases.user.register_user import RegisterUserUseCase
from blog.usecases.user.login_user import LoginUserUseCase
from blog.usecases.user.logout_user import LogoutUserUseCase
from blog.usecases.user.get_current_user import GetCurrentUserUseCase
from blog.usecases.user.set_current_user import SetCurrentUserUseCase


def create_test_user() -> User:
    return User(
        id=str(uuid.uuid4()),
        name="Test User",
        email=Email("test@example.com"),
        password=Password("secur3@Pass"),
        role="user",
    )


def test_register_user():
    repo = InMemoryUserRepository()
    usecase = RegisterUserUseCase(repo)
    user = create_test_user()

    result = usecase.execute(user)

    assert result == user
    assert repo.get_current_user() == user


def test_login_user_success():
    repo = InMemoryUserRepository()
    user = create_test_user()
    repo.register(user)

    usecase = LoginUserUseCase(repo)
    result = usecase.execute(user.email, user.password)

    assert result == user
    assert repo.get_current_user() == user


def test_login_user_failure():
    repo = InMemoryUserRepository()
    usecase = LoginUserUseCase(repo)
    email = Email("notfound@example.com")
    password = Password("wrongP@1ss")

    result = usecase.execute(email, password)

    assert result is None
    assert repo.get_current_user() is None


def test_logout_user():
    repo = InMemoryUserRepository()
    user = create_test_user()
    repo.register(user)
    repo.login(user.email, user.password)

    usecase = LogoutUserUseCase(repo)
    usecase.execute()

    assert repo.get_current_user() is None


def test_get_current_user():
    repo = InMemoryUserRepository()
    user = create_test_user()
    repo.register(user)

    usecase = GetCurrentUserUseCase(repo)
    result = usecase.execute()

    assert result == user


def test_set_current_user():
    repo = InMemoryUserRepository()
    user = create_test_user()

    usecase = SetCurrentUserUseCase(repo)
    usecase.execute(user)

    assert repo.get_current_user() == user
