from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class WeekBase(BaseModel):
    """Schema base para os dados de abastecimento de combustível."""
    title: str = Field(..., description="Título do registro de abastecimento")
    kmAtual: float = Field(..., description="Quilometragem atual do veículo")
    litrosAbastecidos: float = Field(..., description="Quantidade de litros abastecidos")
    custo: float = Field(..., description="Custo total do abastecimento")


class WeekCreate(WeekBase):
    """Schema para criação de um novo registro de abastecimento."""
    user_id: Optional[str] = Field(None, description="ID do usuário (preenchido automaticamente)")
    kmFinal: Optional[float] = Field(None, description="Quilometragem final do veículo")
    eficiencia: Optional[float] = Field(None, description="Eficiência em km/l")


class WeekUpdate(WeekBase):
    """Schema para atualização de um registro existente."""
    kmFinal: Optional[float] = Field(None, description="Quilometragem final do veículo")
    eficiencia: Optional[float] = Field(None, description="Eficiência em km/l (calculada automaticamente)")


class WeekFinalKm(BaseModel):
    """Schema para adicionar apenas a quilometragem final."""
    final_km: float


class WeekResponse(WeekBase):
    """Schema para resposta com dados completos de um registro."""
    id: str = Field(..., description="ID único do registro")
    user_id: str = Field(..., description="ID do usuário que criou o registro")
    kmFinal: Optional[float] = Field(None, description="Quilometragem final do veículo")
    eficiencia: Optional[float] = Field(None, description="Eficiência em km/l")
    created_at: datetime = Field(..., description="Data de criação do registro")
    updated_at: datetime = Field(..., description="Data da última atualização")

    class Config:
        orm_mode = True
        from_attributes = True


class WeekAnalytics(BaseModel):
    """Schema para análise de dados de combustível."""
    media_eficiencia: Optional[float] = Field(None, description="Eficiência média em km/l")
    total_custo: float = Field(..., description="Custo total com combustível")
    total_distancia: float = Field(..., description="Distância total percorrida")
    total_litros: float = Field(..., description="Total de litros abastecidos")