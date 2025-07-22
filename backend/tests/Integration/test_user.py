import pytest
from httpx import AsyncClient

@pytest.mark.asyncio
async def test_register_user(client: AsyncClient):
    response = await client.post("/users/register", json={
        "name": "Test User",
        "email": "test@example.com",
        "password": "SecurePassword123!", 
        "role": "user"
    })
    
    # Print response details for debugging
    print(f"Response status: {response.status_code}")
    print(f"Response body: {response.json()}")
    
    assert response.status_code == 201
    assert response.json()["message"] == "User registered successfully"


@pytest.mark.asyncio
async def test_register_user_existing_email(client: AsyncClient):
    """Testa a tentativa de registrar um usuário com email já existente"""
    # Primeiro, registre um usuário
    await client.post("/users/register", json={
        "name": "Test User",
        "email": "duplicate@example.com",
        "password": "SecurePassword123!", 
        "role": "user"
    })
    
    # Tente registrar outro usuário com o mesmo email
    response = await client.post("/users/register", json={
        "name": "Another User",
        "email": "duplicate@example.com",
        "password": "AnotherPassword123!", 
        "role": "user"
    })
    
    assert response.status_code == 400
    assert "já está registrado" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_register_user_invalid_password(client: AsyncClient):
    """Testa o registro de usuário com senha inválida"""
    response = await client.post("/users/register", json={
        "name": "Invalid Password User",
        "email": "invalid_password@example.com",
        "password": "weak", 
        "role": "user"
    })
    
    print(f"Invalid password response: {response.status_code}, {response.json()}")
    
    assert response.status_code in [400, 422]  # Pydantic validation returns 422, application validation returns 400
    
    # Check for any error message related to password
    response_json = response.json()
    if isinstance(response_json, dict) and "detail" in response_json:
        if isinstance(response_json["detail"], list):
            # Handle case where detail is a list (Pydantic validation)
            for error in response_json["detail"]:
                if isinstance(error, dict) and "msg" in error:
                    if "password" in error.get("msg", "").lower() or "senha" in error.get("msg", "").lower():
                        assert True
                        return
        else:
            # Handle case where detail is a string
            assert "password" in response_json["detail"].lower() or "senha" in response_json["detail"].lower()
    else:
        # For other error formats
        assert "password" in str(response_json).lower() or "senha" in str(response_json).lower() or "value_error" in str(response_json).lower()


@pytest.mark.asyncio
async def test_register_user_invalid_email(client: AsyncClient):
    """Testa o registro de usuário com email inválido"""
    response = await client.post("/users/register", json={
        "name": "Invalid Email User",
        "email": "not-an-email", 
        "password": "ValidPassword123!", 
        "role": "user"
    })
    
    print(f"Invalid email response: {response.status_code}, {response.json()}")
    
    assert response.status_code in [400, 422]  # Pydantic validation returns 422
    
    # Check for any error message related to email
    response_json = response.json()
    if isinstance(response_json, dict) and "detail" in response_json:
        if isinstance(response_json["detail"], list):
            # Handle case where detail is a list (Pydantic validation)
            for error in response_json["detail"]:
                if isinstance(error, dict) and "msg" in error:
                    if "email" in error.get("msg", "").lower():
                        assert True
                        return
        else:
            # Handle case where detail is a string
            assert "email" in response_json["detail"].lower()
    else:
        # For other error formats
        assert "email" in str(response_json).lower() or "value_error" in str(response_json).lower()


@pytest.mark.asyncio
async def test_login_user(client: AsyncClient):
    """Testa o login de usuário com credenciais válidas"""
    # Registre um usuário primeiro
    email = "login_test@example.com"
    password = "LoginPass123!"
    
    await client.post("/users/register", json={
        "name": "Login Test User",
        "email": email,
        "password": password, 
        "role": "user"
    })    # Tente fazer login
    response = await client.post("/users/login", json={
        "email": email,
        "password": password
    })
    
    print(f"Login response: {response.status_code} - {response.text}")
    
    assert response.status_code == 200
    assert "access_token" in response.json()
    assert "token_type" in response.json()
    assert response.json()["token_type"] == "bearer"


@pytest.mark.asyncio
async def test_login_user_invalid_credentials(client: AsyncClient):
    """Testa o login de usuário com credenciais inválidas"""
    # Tente fazer login com credenciais inválidas
    response = await client.post("/users/login", json={
        "email": "nonexistent@example.com",
        "password": "WrongPassword123!"
    })
    
    assert response.status_code == 401
    assert "credenciais inválidas" in response.json()["detail"].lower()


@pytest.mark.asyncio
async def test_login_with_invalid_token(client: AsyncClient):
    """Testa acessar endpoint protegido com token inválido"""
    headers = {"Authorization": "Bearer invalid-token-here"}
    
    response = await client.get("/users/me", headers=headers)
    
    assert response.status_code in [401, 403]
    assert ("não autenticado" in response.json()["detail"].lower() or 
            "forbidden" in response.json()["detail"].lower() or 
            "not authenticated" in response.json()["detail"].lower() or
            "erro de autenticação" in response.json()["detail"].lower())


@pytest.mark.asyncio
async def test_get_current_user(client: AsyncClient):
    """Testa a obtenção do usuário atual após login"""
    # Registre um usuário
    email = "current_user@example.com"
    password = "CurrentUserPass123!"
    name = "Current User Test"
    
    await client.post("/users/register", json={
        "name": name,
        "email": email,
        "password": password, 
        "role": "user"
    })
    
    # Faça login para obter o token
    login_response = await client.post("/users/login", json={
        "email": email,
        "password": password
    })
    
    # Obtenha o token
    token = login_response.json()["access_token"]
    
    # Configure o cabeçalho de autorização
    headers = {"Authorization": f"Bearer {token}"}
    
    # Obtenha o usuário atual
    response = await client.get("/users/me", headers=headers)
    
    assert response.status_code == 200
    assert response.json()["email"] == email
    assert response.json()["name"] == name


@pytest.mark.asyncio
async def test_get_current_user_no_token(client: AsyncClient):
    """Testa a tentativa de obter o usuário atual sem token de autenticação"""
    response = await client.get("/users/me")
    
    assert response.status_code in [401, 403]  # Pode ser 401 (Unauthorized) ou 403 (Forbidden)
    assert "not authenticated" in response.json()["detail"].lower() or "forbidden" in response.json()["detail"].lower()
