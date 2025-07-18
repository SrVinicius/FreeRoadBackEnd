# import pytest
# from fastapi.testclient import TestClient
# from freeroad.api.main import app

# @pytest.fixture(scope="function")
# def client():
#     return TestClient(app)

# @pytest.mark.asyncio
# async def test_register_and_login(client):
#     """
#     Testa o registro, login e recuperação de informações do usuário.
#     """
#     # Registro
#     response = client.post(
#         "/users/register",
#         json={
#             "name": "Test User",
#             "email": "test@example.com",
#             "password": "test@A123",
#             "role": "user",
#         },
#     )
#     assert response.status_code == 201
#     data = response.json()
#     assert data["message"] == "User registered successfully"
#     assert "user" in data
#     assert data["user"]["email"] == "test@example.com"

#     # Login
#     response = client.post(
#         "/users/login", json={"email": "test@example.com", "password": "test@A123"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert "access_token" in data
#     token = data["access_token"]

#     # GET /users/me
#     response = client.get(
#         "/users/me", headers={"Authorization": f"Bearer {token}"}
#     )
#     assert response.status_code == 200
#     data = response.json()
#     assert data["email"] == "test@example.com"
#     assert data["name"] == "Test User"
#     assert data["role"] == "user"


# @pytest.mark.asyncio
# async def test_register_with_existing_email(client):
#     """
#     Testa o registro com um email já existente.
#     """
#     # Registro inicial
#     client.post(
#         "/users/register",
#         json={
#             "name": "Test User",
#             "email": "duplicate@example.com",
#             "password": "test@A123",
#             "role": "user",
#         },
#     )

#     # Registro com o mesmo email
#     response = client.post(
#         "/users/register",
#         json={
#             "name": "Another User",
#             "email": "duplicate@example.com",
#             "password": "another@A123",
#             "role": "user",
#         },
#     )
#     assert response.status_code == 400
#     data = response.json()
#     assert data["detail"] == "Email já está registrado."


# @pytest.mark.asyncio
# async def test_login_with_invalid_credentials(client):
#     """
#     Testa o login com credenciais inválidas.
#     """
#     response = client.post(
#         "/users/login", json={"email": "invalid@example.com", "password": "wrong@123"}
#     )
#     assert response.status_code == 401
#     data = response.json()
#     assert data["detail"] == "Credenciais inválidas."


# @pytest.mark.asyncio
# async def test_access_protected_route_without_token(client):
#     """
#     Testa o acesso a uma rota protegida sem fornecer o token.
#     """
#     response = client.get("/users/me")
#     assert response.status_code == 403
#     data = response.json()
#     assert data["detail"] == "Not authenticated"