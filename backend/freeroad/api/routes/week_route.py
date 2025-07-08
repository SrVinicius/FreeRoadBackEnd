from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Optional
from uuid import uuid4

from freeroad.domain.entities.week import Week
from freeroad.api.deps import get_week_repository
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


@router.get("/", response_model=List[WeekResponse])
def get_all_weeks(week_repo=Depends(get_week_repository)):
    """
    Retorna todos os registros de abastecimento.
    """
    usecase = GetAllWeeksUseCase(week_repo)
    weeks = usecase.execute()
    return weeks


@router.get("/{week_id}", response_model=WeekResponse)
def get_week_by_id(week_id: str, week_repo=Depends(get_week_repository)):
    """
    Retorna um registro de abastecimento específico pelo ID.
    """
    usecase = GetWeekByIdUseCase(week_repo)
    week = usecase.execute(week_id)
    if not week:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro não encontrado"
        )
    return week


@router.get("/user/{user_id}", response_model=List[WeekResponse])
def get_weeks_by_user_id(user_id: str, week_repo=Depends(get_week_repository)):
    """
    Retorna todos os registros de abastecimento de um usuário específico.
    """
    usecase = GetWeeksByUserIdUseCase(week_repo)
    weeks = usecase.execute(user_id)
    return weeks


@router.post("/", response_model=WeekResponse, status_code=status.HTTP_201_CREATED)
def create_week(week_data: WeekCreate, week_repo=Depends(get_week_repository)):
    """
    Cria um novo registro de abastecimento.
    """
    week = Week(
        id=str(uuid4()),
        user_id=week_data.user_id,
        title=week_data.title,
        kmAtual=str(week_data.kmAtual),
        kmFinal="0",  # Será atualizado posteriormente
        custo=str(week_data.custo),
        eficiencia="0",  # Será calculado posteriormente
        litrosAbastecidos=str(week_data.litrosAbastecidos)
    )
    
    usecase = CreateWeekUseCase(week_repo)
    created_week = usecase.execute(week)
    
    if not created_week:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não foi possível criar o registro"
        )
    
    return created_week


@router.delete("/{week_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_week(week_id: str, week_repo=Depends(get_week_repository)):
    """
    Remove um registro de abastecimento.
    """
    usecase = DeleteWeekUseCase(week_repo)
    usecase.execute(week_id)
    return None


@router.patch("/{week_id}/final-km", response_model=WeekResponse)
def add_final_km(week_id: str, data: WeekFinalKm, week_repo=Depends(get_week_repository)):
    """
    Adiciona a quilometragem final e calcula a eficiência.
    """
    usecase = AddFinalKmUseCase(week_repo)
    updated_week = usecase.execute(week_id, data.kmFinal)
    
    if not updated_week:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro não encontrado"
        )
    
    return updated_week


@router.get("/user/{user_id}/efficiency", response_model=float)
def get_average_efficiency(user_id: str, week_repo=Depends(get_week_repository)):
    """
    Calcula a eficiência média de combustível para um usuário.
    """
    usecase = CalculateAverageEfficiencyUseCase(week_repo)
    efficiency = usecase.execute(user_id)
    
    if efficiency is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Nenhum dado de eficiência encontrado para este usuário"
        )
    
    return efficiency