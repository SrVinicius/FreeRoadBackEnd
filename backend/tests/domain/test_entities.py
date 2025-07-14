import pytest
from freeroad.domain.entities.week import Week
from freeroad.domain.entities.user import User
from freeroad.domain.value_objects.email_vo import Email
from freeroad.domain.value_objects.password import Password, PasswordValidationError


def test_create_user():
    """
    Testa a criação de um usuário válido.
    """
    email = Email("user@example.com")
    pwd = Password("Secret@123")
    user = User("1", "User", email, pwd, "user")
    assert user.name == "User"
    assert user.email.value == "user@example.com"
    assert user.role == "user"


def test_invalid_role():
    """
    Testa a criação de um usuário com um papel inválido.
    """
    with pytest.raises(ValueError):
        User("1", "User", Email("user@example.com"), Password("Secret@123"), "invalid")


def test_create_week():
    """
    Testa a criação de um registro de abastecimento válido.
    """
    week = Week(
        id="1",
        user_id="user1",
        title="Abastecimento Teste",
        kmAtual="1000",
        kmFinal="1500",
        custo="300",
        eficiencia="10.0",
        litrosAbastecidos="50",
        created_at="2024-01-01",
        updated_at="2024-01-02",
    )
    assert week.title == "Abastecimento Teste"
    assert week.kmAtual == "1000"
    assert week.kmFinal == "1500"
    assert week.custo == "300"
    assert week.eficiencia == "10.0"
    assert week.litrosAbastecidos == "50"


def test_invalid_email():
    """
    Testa a criação de um email inválido.
    """
    with pytest.raises(ValueError):
        Email("invalid-email")


def test_invalid_password():
    """
    Testa a criação de uma senha inválida.
    """
    with pytest.raises(PasswordValidationError):
        Password("weak")