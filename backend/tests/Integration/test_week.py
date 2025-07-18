# import pytest
# from fastapi.testclient import TestClient
# from freeroad.api.main import app
# from freeroad.infra.repositories.in_memory_week_repository import InMemoryWeekRepository
# from freeroad.api.deps import get_week_repository, get_current_user
# from datetime import datetime
# import uuid

# class FakeUser:
#     def __init__(self):
#         self.id = str(uuid.uuid4())
#         self.name = "Test User"
#         self.email = type("Email", (), {"value": "test@example.com"})()
#         self.role = "user"
#         self.token = f"Bearer {self.id}"  # Generate a valid token

# @pytest.fixture(scope="function")
# def client():
#     repo = InMemoryWeekRepository()
#     fake_user = FakeUser()
#     app.dependency_overrides[get_week_repository] = lambda: repo
#     app.dependency_overrides[get_current_user] = lambda: fake_user
#     return TestClient(app), fake_user.token

# def create_week_payload(user_id=None):
#     return {
#         "id": str(uuid.uuid4()),
#         "user_id": user_id or str(uuid.uuid4()),
#         "title": "Semana de Teste",
#         "kmAtual": "1000",
#         "kmFinal": "1500",
#         "custo": "300",
#         "eficiencia": "10.0",
#         "litrosAbastecidos": "50",
#         "created_at": datetime.now().isoformat(),
#         "updated_at": datetime.now().isoformat(),
#     }

# def test_create_week(client):
#     client, token = client
#     payload = create_week_payload()
#     headers = {"Authorization": "Bearer fake_token"}  # Simulate authenticated user
#     response = client.post("/weeks/", json=payload, headers=headers)
#     assert response.status_code == 201
#     data = response.json()
#     assert data["title"] == payload["title"]
#     assert float(data["kmAtual"]) == float(payload["kmAtual"])

# def test_get_all_weeks(client):
#     client, token = client  # Unpack the client and token
#     payload1 = create_week_payload()
#     payload2 = create_week_payload()
#     headers = {"Authorization": token}  # Use the valid token from the fixture
#     resp1 = client.post("/weeks/", json=payload1, headers=headers)
#     resp2 = client.post("/weeks/", json=payload2, headers=headers)
#     id1 = resp1.json()["id"]
#     id2 = resp2.json()["id"]
#     response = client.get("/weeks/", headers=headers)
#     assert response.status_code == 200
#     data = response.json()
#     assert isinstance(data, list)
#     assert any(week["id"] == id1 for week in data)
#     assert any(week["id"] == id2 for week in data)

# # def test_get_week_by_id(client):
# #     payload = create_week_payload()
# #     headers = {"Authorization": "Bearer fake_token"}  # Simulate authenticated user
# #     post_resp = client.post("/weeks/", json=payload, headers=headers)
# #     week_id = post_resp.json()["id"]
# #     response = client.get(f"/weeks/{week_id}", headers=headers)
# #     assert response.status_code == 200
# #     data = response.json()
# #     assert data["id"] == week_id

# # def test_delete_week(client):
# #     payload = create_week_payload()
# #     headers = {"Authorization": "Bearer fake_token"}  # Simulate authenticated user
# #     post_resp = client.post("/weeks/", json=payload, headers=headers)
# #     week_id = post_resp.json()["id"]
# #     response = client.delete(f"/weeks/{week_id}", headers=headers)
# #     assert response.status_code == 204
# #     # Confirm deletion
# #     response = client.get(f"/weeks/{week_id}", headers=headers)
# #     assert response.status_code == 404

# # def test_get_weeks_by_user_id(client):
# #     user_id = str(uuid.uuid4())
# #     payload1 = create_week_payload(user_id=user_id)
# #     payload2 = create_week_payload(user_id=user_id)
# #     headers = {"Authorization": "Bearer fake_token"}  # Simulate authenticated user
# #     client.post("/weeks/", json=payload1, headers=headers)
# #     client.post("/weeks/", json=payload2, headers=headers)
# #     response = client.get(f"/weeks/user/{user_id}", headers=headers)
# #     assert response.status_code == 200
# #     data = response.json()
# #     assert isinstance(data, list)
# #     assert all(week["user_id"] == user_id for week in data)

# # def test_add_final_km(client):
# #     payload = create_week_payload()
# #     headers = {"Authorization": "Bearer fake_token"}  # Simulate authenticated user
# #     post_resp = client.post("/weeks/", json=payload, headers=headers)
# #     week_id = post_resp.json()["id"]
# #     response = client.put(f"/weeks/{week_id}/final_km", json={"final_km": 2000}, headers=headers)
# #     assert response.status_code == 200
# #     data = response.json()
# #     assert float(data["kmFinal"]) == 2000.0

# # def test_calculate_average_efficiency(client):
# #     user_id = str(uuid.uuid4())
# #     payload1 = create_week_payload(user_id=user_id)
# #     payload2 = create_week_payload(user_id=user_id)
# #     payload1["eficiencia"] = "15.0"
# #     payload2["eficiencia"] = "25.0"
# #     headers = {"Authorization": "Bearer fake_token"}  # Simulate authenticated user
# #     client.post("/weeks/", json=payload1, headers=headers)
# #     client.post("/weeks/", json=payload2, headers=headers)
# #     response = client.get(f"/weeks/{user_id}/average_efficiency", headers=headers)
# #     assert response.status_code == 200
# #     data = response.json()
# #     assert float(data["average_efficiency"]) == 20.0