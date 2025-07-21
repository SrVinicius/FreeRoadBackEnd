import pytest
import uuid
from datetime import datetime
from freeroad.domain.entities.week import Week
from freeroad.domain.entities.user import User
from freeroad.domain.value_objects.email_vo import Email
from freeroad.domain.value_objects.password import Password
from freeroad.usecases.week.create_week import CreateWeekUseCase
from freeroad.usecases.week.get_all import GetAllWeeksUseCase
from freeroad.usecases.week.get_by_id import GetWeekByIdUseCase
from freeroad.usecases.week.get_by_user_id import GetWeeksByUserIdUseCase
from freeroad.usecases.week.delete_week import DeleteWeekUseCase
from freeroad.usecases.week.add_final_km import AddFinalKmUseCase
# Importação temporariamente comentada devido a problemas de importação
# from freeroad.usecases.week.calculate_average_efficiency import CalculateAverageEfficiencyUseCase
from freeroad.infra.repositories.sqlalchemy.sqlalchemy_user_repository import SQLAlchemyUserRepository


def create_test_week(user_id: str) -> Week:
    """Cria um registro de abastecimento para testes"""
    return Week(
        id=str(uuid.uuid4()),
        user_id=user_id,
        title="Abastecimento Teste",
        kmAtual="1000",
        kmFinal="0",  # Começa sem km final
        custo="150.00",
        eficiencia="0",  # Começa sem eficiência calculada
        litrosAbastecidos="30.5",
        created_at=datetime.now(),
        updated_at=datetime.now()
    )


@pytest.mark.asyncio
async def test_create_week_success(week_repository, test_user):
    """Testa o caso de uso de criação de registro de abastecimento com sucesso"""
    usecase = CreateWeekUseCase(week_repository)

    week = create_test_week(test_user.id)
    result = await usecase.execute(week)

    assert result is not None
    assert result.id == week.id
    assert result.title == week.title
    
    # Verificar se o week foi realmente salvo no banco
    saved_week = await week_repository.get_by_id(week.id)
    assert saved_week is not None
    assert saved_week.id == week.id


@pytest.mark.asyncio
async def test_get_all_weeks(week_repository, test_user):
    """Testa o caso de uso para obter todos os registros de abastecimento"""
    # Limpar registros existentes para ter um estado conhecido
    all_weeks = await week_repository.get_all()
    for week in all_weeks:
        await week_repository.delete(week.id)
    
    # Adicionar registros de teste
    week1 = create_test_week(test_user.id)
    week2 = create_test_week(test_user.id)
    week3 = create_test_week(test_user.id)
    
    await week_repository.create(week1)
    await week_repository.create(week2)
    await week_repository.create(week3)
    
    # Testar o caso de uso
    usecase = GetAllWeeksUseCase(week_repository)
    result = await usecase.execute()
    
    assert len(result) >= 3  # Pode haver outros registros no banco
    
    # Verificar se nossos registros estão no resultado
    result_ids = [w.id for w in result]
    assert week1.id in result_ids
    assert week2.id in result_ids
    assert week3.id in result_ids


@pytest.mark.asyncio
async def test_get_week_by_id(week_repository, test_user):
    """Testa o caso de uso para obter um registro de abastecimento pelo ID"""
    # Adiciona um registro
    week = create_test_week(test_user.id)
    created_week = await week_repository.create(week)
    
    usecase = GetWeekByIdUseCase(week_repository)
    result = await usecase.execute(created_week.id)
    
    assert result is not None
    assert result.id == created_week.id
    assert result.title == created_week.title


@pytest.mark.asyncio
async def test_get_week_by_id_not_found(week_repository):
    """Testa o caso de uso para obter um registro de abastecimento com ID inexistente"""
    usecase = GetWeekByIdUseCase(week_repository)
    
    result = await usecase.execute("id-inexistente")
    
    assert result is None


@pytest.mark.asyncio
async def test_get_weeks_by_user_id(week_repository, db_session):
    """Testa o caso de uso para obter registros de abastecimento de um usuário específico"""
    # Criamos dois usuários diferentes para o teste
    user_repo = SQLAlchemyUserRepository(db_session)
    
    user1 = User(
        id=str(uuid.uuid4()),
        name="User Test 1",
        email=Email("user1@test.com"),
        password=Password("Senha@123"),
        role="user"
    )
    
    user2 = User(
        id=str(uuid.uuid4()),
        name="User Test 2",
        email=Email("user2@test.com"),
        password=Password("Senha@123"),
        role="user"
    )
    
    await user_repo.register(user1)
    await user_repo.register(user2)
    
    # Adiciona registros para diferentes usuários
    week1 = create_test_week(user1.id)
    week2 = create_test_week(user1.id)
    week3 = create_test_week(user2.id)
    
    await week_repository.create(week1)
    await week_repository.create(week2)
    await week_repository.create(week3)
    
    usecase = GetWeeksByUserIdUseCase(week_repository)
    result = await usecase.execute(user1.id)
    
    # Verificamos que temos pelo menos 2 registros do user1
    assert len(result) >= 2
    
    # Verificamos que todos os registros retornados são do user1
    for week in result:
        assert week.user_id == user1.id


@pytest.mark.asyncio
async def test_delete_week(week_repository, test_user):
    """Testa o caso de uso para remover um registro de abastecimento"""
    # Adiciona um registro
    week = create_test_week(test_user.id)
    created_week = await week_repository.create(week)
    
    # Verifica que o registro existe
    assert await week_repository.get_by_id(created_week.id) is not None
    
    # Remove o registro
    usecase = DeleteWeekUseCase(week_repository)
    await usecase.execute(created_week.id)
    
    # Verifica que o registro foi removido
    assert await week_repository.get_by_id(created_week.id) is None


@pytest.mark.asyncio
async def test_add_final_km(week_repository, test_user):
    """Testa o caso de uso para adicionar quilometragem final e calcular eficiência"""
    # Cria um registro com km inicial 1000 e 30.5 litros
    week = create_test_week(test_user.id)
    week.kmAtual = "1000"
    week.litrosAbastecidos = "30.5"
    
    created_week = await week_repository.create(week)
    
    # Adiciona quilometragem final (1500 km)
    usecase = AddFinalKmUseCase(week_repository)
    final_km = 1500.0
    result = await usecase.execute(created_week.id, final_km)
    
    # Verifica que a quilometragem final foi atualizada
    assert float(result.kmFinal) == final_km
    
    # Verifica que a eficiência foi calculada corretamente
    # Eficiência = (1500 - 1000) / 30.5 = 16.39 km/l
    expected_efficiency = round((final_km - float(week.kmAtual)) / float(week.litrosAbastecidos), 2)
    assert float(result.eficiencia) == expected_efficiency
    
    # Verificar se as mudanças foram persistidas no banco
    updated_week = await week_repository.get_by_id(created_week.id)
    assert float(updated_week.kmFinal) == final_km
    assert float(updated_week.eficiencia) == expected_efficiency


@pytest.mark.asyncio
async def test_add_final_km_not_found(week_repository):
    """Testa o caso de uso para adicionar quilometragem final a um registro inexistente"""
    usecase = AddFinalKmUseCase(week_repository)
    
    result = await usecase.execute("id-inexistente", 1500.0)
    
    assert result is None




