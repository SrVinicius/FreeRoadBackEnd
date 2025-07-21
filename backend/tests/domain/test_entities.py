import pytest
from freeroad.domain.entities.week import Week
from freeroad.domain.entities.user import User
from freeroad.domain.value_objects.email_vo import Email
from freeroad.domain.value_objects.password import Password


def test_create_user():
    email = Email("exemplo@gmail.com.br")
    senha = Password("Password@123")
    user = User(id="123", name="Test User", email=email, password=senha, role="user")

    assert user.id == "123"
    assert user.name == "Test User"
    assert user.email == email
    assert user.password == senha
    assert user.role == "user"

def test_create_week():
    week = Week(
        id="456", 
        user_id="123", 
        title="teste week", 
        kmAtual="1500",
        kmFinal="1700",
        custo="120",
        eficiencia="",
        litrosAbastecidos="9",     
    )

    assert week.id == "456"
    assert week.user_id == "123"
    assert week.title == "teste week"
    assert week.kmAtual == "1500"
    assert week.kmFinal == "1700"
    assert week.custo == "120"
    assert week.eficiencia == ""
    assert week.litrosAbastecidos == "9"
