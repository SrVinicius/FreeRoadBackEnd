# import uuid
# import pytest
# from freeroad.domain.entities.week import Week
# from freeroad.infra.repositories.in_memory_week_repository import InMemoryWeekRepository
# from freeroad.usecases.week.create_week import CreateWeekUseCase
# from freeroad.usecases.week.get_all import GetAllWeeksUseCase
# from freeroad.usecases.week.get_by_id import GetWeekByIdUseCase
# from freeroad.usecases.week.get_by_user_id import GetWeeksByUserIdUseCase
# from freeroad.usecases.week.delete_week import DeleteWeekUseCase
# from freeroad.usecases.week.add_final_km import AddFinalKmUseCase
# from freeroad.usecases.week.calculate_average_efficiency import CalculateAverageEfficiencyUseCase


# def create_test_week() -> Week:
#     """
#     Cria um registro de abastecimento de teste.
#     """
#     return Week(
#         id=str(uuid.uuid4()),
#         user_id=str(uuid.uuid4()),
#         title="Semana de Teste",
#         kmAtual="1000",
#         kmFinal="1500",
#         custo="300",
#         eficiencia="10.0",
#         litrosAbastecidos="50",
#         created_at="2025-07-14",
#         updated_at="2025-07-14",
#     )


# @pytest.mark.asyncio
# async def test_create_week():
#     repo = InMemoryWeekRepository()
#     usecase = CreateWeekUseCase(repo)
#     week = create_test_week()

#     result = await usecase.execute(week)

#     assert result == week
#     assert await repo.get_by_id(week.id) == week


# @pytest.mark.asyncio
# async def test_get_all_weeks():
#     repo = InMemoryWeekRepository()
#     week1 = create_test_week()
#     week2 = create_test_week()
#     await repo.create(week1)
#     await repo.create(week2)

#     usecase = GetAllWeeksUseCase(repo)
#     result = await usecase.execute()

#     assert len(result) == 2
#     assert week1 in result
#     assert week2 in result


# @pytest.mark.asyncio
# async def test_get_week_by_id():
#     repo = InMemoryWeekRepository()
#     week = create_test_week()
#     await repo.create(week)

#     usecase = GetWeekByIdUseCase(repo)
#     result = await usecase.execute(week.id)

#     assert result == week


# @pytest.mark.asyncio
# async def test_get_weeks_by_user_id():
#     repo = InMemoryWeekRepository()
#     user_id = str(uuid.uuid4())
#     week1 = create_test_week()
#     week2 = create_test_week()
#     week1.user_id = user_id
#     week2.user_id = user_id
#     await repo.create(week1)
#     await repo.create(week2)

#     usecase = GetWeeksByUserIdUseCase(repo)
#     result = await usecase.execute(user_id)

#     assert len(result) == 2
#     assert week1 in result
#     assert week2 in result


# @pytest.mark.asyncio
# async def test_delete_week():
#     repo = InMemoryWeekRepository()
#     week = create_test_week()
#     await repo.create(week)

#     usecase = DeleteWeekUseCase(repo)
#     await usecase.execute(week.id)

#     assert await repo.get_by_id(week.id) is None


# @pytest.mark.asyncio
# async def test_add_final_km():
#     repo = InMemoryWeekRepository()
#     week = create_test_week()
#     await repo.create(week)

#     usecase = AddFinalKmUseCase(repo)
#     updated_week = await usecase.execute(week.id, 2000)

#     assert updated_week.kmFinal == "2000"
#     assert updated_week.eficiencia == "20.0"


# @pytest.mark.asyncio
# async def test_calculate_average_efficiency():
#     repo = InMemoryWeekRepository()
#     user_id = str(uuid.uuid4())
#     week1 = create_test_week()
#     week2 = create_test_week()
#     week1.user_id = user_id
#     week2.user_id = user_id
#     week1.eficiencia = "15.0"
#     week2.eficiencia = "25.0"
#     await repo.create(week1)
#     await repo.create(week2)

#     usecase = CalculateAverageEfficiencyUseCase(repo)
#     result = await usecase.execute(user_id)

#     assert result == 20.0