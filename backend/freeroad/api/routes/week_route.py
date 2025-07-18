from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import uuid4
from datetime import datetime
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials

from freeroad.domain.entities.week import Week
from freeroad.api.deps import get_week_repository, get_user_repository
from freeroad.usecases.week.get_all import GetAllWeeksUseCase
from freeroad.usecases.week.get_by_id import GetWeekByIdUseCase
from freeroad.usecases.week.get_by_user_id import GetWeeksByUserIdUseCase
from freeroad.usecases.week.create_week import CreateWeekUseCase
from freeroad.usecases.week.delete_week import DeleteWeekUseCase
from freeroad.usecases.week.add_final_km import AddFinalKmUseCase
from freeroad.usecases.week.calculate_average_efficiency import CalculateAverageEfficiencyUseCase

# Import schemas if you have them
from freeroad.api.schemas.week_schema import (
    WeekCreate, 
    WeekResponse, 
    WeekUpdate,
    WeekFinalKm
)

router = APIRouter()

security = HTTPBearer()

async def get_current_user_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    user_repo=Depends(get_user_repository)  # Certifique-se de usar o repositório correto
):
    token = credentials.credentials
    # Simula a lógica de autenticação para os testes
    user = await user_repo.get_current_user()
    if not user or user.id != token:
        raise HTTPException(status_code=401, detail="Usuário não autenticado.")
    return user

# Todas as rotas protegidas abaixo:
@router.get("/", response_model=List[WeekResponse])
async def get_all_weeks(
    week_repo=Depends(get_week_repository),
    user=Depends(get_current_user_token)
):
    """
    Retorna todos os registros de abastecimento.
    """
    try:
        usecase = GetAllWeeksUseCase(week_repo)
        weeks = await usecase.execute()
        print(f"Debug: Found {len(weeks) if weeks else 0} weeks")
        print(f"Debug: Week types: {[type(w) for w in weeks] if weeks else []}")
        return weeks
    except Exception as e:
        import traceback
        print(f"Error in get_all_weeks: {str(e)}")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/{week_id}", response_model=WeekResponse)
async def get_week_by_id(
    week_id: str,
    week_repo=Depends(get_week_repository),
    user=Depends(get_current_user_token)
):
    """
    Retorna um registro de abastecimento específico pelo ID.
    """
    usecase = GetWeekByIdUseCase(week_repo)
    week = await usecase.execute(week_id)
    if not week:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro não encontrado"
        )
    return week


@router.get("/user/{user_id}", response_model=List[WeekResponse])
async def get_weeks_by_user_id(
    user_id: str,
    week_repo=Depends(get_week_repository),
    user=Depends(get_current_user_token)
):
    """
    Retorna todos os registros de abastecimento de um usuário específico.
    """
    usecase = GetWeeksByUserIdUseCase(week_repo)
    weeks = await usecase.execute(user_id)
    return weeks


@router.post("/", response_model=WeekResponse, status_code=status.HTTP_201_CREATED)
async def create_week(
    week_data: WeekCreate,
    week_repo=Depends(get_week_repository)
):
    week = Week(
        id=str(uuid4()),
        user_id=week_data.user_id or "",  # Ensure user_id is a string
        title=week_data.title,
        kmAtual=str(week_data.kmAtual),
        kmFinal=str(week_data.kmFinal) if hasattr(week_data, "kmFinal") else "0",
        custo=str(week_data.custo),
        eficiencia=str(week_data.eficiencia) if week_data.eficiencia else "0",  # Default to "0" if None
        litrosAbastecidos=str(week_data.litrosAbastecidos),
        created_at=datetime.now(),  # Use datetime object
        updated_at=datetime.now(),  # Use datetime object
    )
    usecase = CreateWeekUseCase(week_repo)
    created_week = await usecase.execute(week)
    return created_week


@router.delete("/{week_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_week(
    week_id: str,
    week_repo=Depends(get_week_repository),
    user=Depends(get_current_user_token)
):
    """
    Remove um registro de abastecimento.
    """
    usecase = DeleteWeekUseCase(week_repo)
    await usecase.execute(week_id)
    return None


@router.put("/{week_id}/final_km", response_model=WeekResponse)
async def add_final_km(
    week_id: str,
    data: WeekFinalKm,
    week_repo=Depends(get_week_repository),
    user=Depends(get_current_user_token)
):
    """
    Adiciona a quilometragem final e calcula a eficiência.
    """
    usecase = AddFinalKmUseCase(week_repo)
    updated_week = await usecase.execute(week_id, data.final_km)
    
    if not updated_week:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro não encontrado"
        )
    
    return updated_week


@router.get("/{user_id}/average_efficiency")
async def get_average_efficiency(
    user_id: str,
    week_repo=Depends(get_week_repository),
    user=Depends(get_current_user_token)
):
    """
    Calcula a eficiência média de combustível para um usuário.
    """
    usecase = CalculateAverageEfficiencyUseCase(week_repo)
    efficiency = await usecase.execute(user_id)
    
    if efficiency is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum dado de eficiência encontrado para este usuário"
        )
    
    return {"average_efficiency": efficiency}