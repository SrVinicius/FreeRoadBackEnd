# import pytest
# from httpx import AsyncClient

# @pytest.mark.asyncio
# async def test_register_user(client: AsyncClient):
#     response = await client.post("/users/register", json={
#         "name": "Test User",
#         "email": "test@example.com",
#         "password": "SecurePassword123!",  # Add a special character to the password
#         "role": "user"
#     })
    
#     # Print response details for debugging
#     print(f"Response status: {response.status_code}")
#     print(f"Response body: {response.json()}")
    
#     assert response.status_code == 201
#     assert response.json()["message"] == "User registered successfully"

