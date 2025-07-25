from typing import List, Optional
from sqlalchemy.orm import joinedload
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import uuid4

from freeroad.domain.entities.week import Week
from freeroad.domain.repositories.week_repository import WeekRepository
from freeroad.infra.models.week_model import WeekModel


class SQLAlchemyWeekRepository(WeekRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_all(self) -> List[Week]:
        result = await self.session.execute(
            select(WeekModel).options(joinedload(WeekModel.user))
        )
        return [week.to_entity() for week in result.scalars().all()]

    async def get_by_id(self, week_id: str) -> Optional[Week]:
        result = await self.session.execute(
            select(WeekModel).options(joinedload(WeekModel.user)).where(WeekModel.id == week_id)
        )
        week = result.scalar_one_or_none()
        return week.to_entity() if week else None

    async def get_by_user_id(self, user_id: str) -> List[Week]:
        result = await self.session.execute(
            select(WeekModel).options(joinedload(WeekModel.user)).where(WeekModel.user_id == user_id)
        )
        return [week.to_entity() for week in result.scalars().all()]

    async def create(self, week: Week) -> Week:
        week_model = WeekModel.from_entity(week)
        self.session.add(week_model)
        await self.session.commit()
        await self.session.refresh(week_model)
        return week_model.to_entity()

    async def update(self, week: Week) -> Optional[Week]:
        result = await self.session.execute(
            select(WeekModel).where(WeekModel.id == week.id)
        )
        week_model = result.scalar_one_or_none()
        if not week_model:
            return None

        week_model.title = week.title
        week_model.km_atual = float(week.kmAtual) 
        week_model.km_final = float(week.kmFinal) 
        week_model.custo = float(week.custo) 
        week_model.eficiencia = float(week.eficiencia) 
        week_model.litros_abastecidos = float(week.litrosAbastecidos) 

        await self.session.commit()
        await self.session.refresh(week_model)
        return week_model.to_entity()

    async def delete(self, week_id: str) -> None:
        result = await self.session.execute(
            select(WeekModel).where(WeekModel.id == week_id)
        )
        week_model = result.scalar_one_or_none()
        if week_model:
            await self.session.delete(week_model)
            await self.session.commit()

    async def add_final_km(self, week_id: str, final_km: float) -> Optional[Week]:
        result = await self.session.execute(
            select(WeekModel).where(WeekModel.id == week_id)
        )
        week_model = result.scalar_one_or_none()
        if not week_model:
            return None

        # Atualiza a quilometragem final
        week_model.km_final = float(final_km)  # Garantir que é float
        
        # Calcula a eficiência de combustível (km/l)
        try:
            # Converter para float para garantir operações consistentes
            km_atual_float = float(week_model.km_atual)
            final_km_float = float(week_model.km_final)
            litros_float = float(week_model.litros_abastecidos)
            
            km_percorrido = final_km_float - km_atual_float
            
            if km_percorrido > 0 and litros_float > 0:
                # Calcula km/l - quilômetros percorridos dividido por litros abastecidos
                eficiencia = km_percorrido / litros_float
                week_model.eficiencia = round(eficiencia, 2)  # Arredonda para 2 casas decimais
                print(f"Eficiência calculada: {eficiencia:.2f} km/l (km_percorrido={km_percorrido}, litros={litros_float})")
            else:
                print(f"Não foi possível calcular eficiência: km_percorrido={km_percorrido}, litros={litros_float}")
                
        except Exception as e:
            print(f"Erro ao calcular eficiência: {str(e)}")
            # Não propagar o erro, apenas logar
        
        await self.session.commit()
        await self.session.refresh(week_model)
        return week_model.to_entity()
