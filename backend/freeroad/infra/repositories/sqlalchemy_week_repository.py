from typing import List, Optional
from sqlalchemy.orm import Session
from uuid import uuid4

from freeroad.domain.entities.week import Week
from freeroad.domain.repositories.week_repository import WeekRepository
from freeroad.infra.models.week_model import WeekModel


class SQLAlchemyWeekRepository(WeekRepository):
    def __init__(self, session: Session):
        self.session = session

    def get_all(self) -> List[Week]:
        week_models = self.session.query(WeekModel).all()
        return [self._model_to_entity(model) for model in week_models]

    def get_by_id(self, week_id: str) -> Optional[Week]:
        week_model = self.session.query(WeekModel).filter(WeekModel.id == week_id).first()
        if not week_model:
            return None
        return self._model_to_entity(week_model)
    
    def get_by_user_id(self, user_id: str) -> List[Week]:
        week_models = self.session.query(WeekModel).filter(WeekModel.user_id == user_id).all()
        return [self._model_to_entity(model) for model in week_models]
    
    def create(self, week: Week) -> Optional[Week]:
        if not week.id:
            week.id = str(uuid4())
            
        week_model = WeekModel(
            id=week.id,
            user_id=week.user_id,
            title=week.title,
            km_atual=week.kmAtual,
            km_final=week.kmFinal,
            custo=week.custo,
            eficiencia=week.eficiencia,
            litros_abastecidos=week.litrosAbastecidos
        )
        
        self.session.add(week_model)
        self.session.commit()
        
        return self._model_to_entity(week_model)

    def update(self, week: Week) -> Optional[Week]:
        week_model = self.session.query(WeekModel).filter(WeekModel.id == week.id).first()
        if not week_model:
            return None
            
        week_model.title = week.title
        week_model.km_atual = week.kmAtual
        week_model.km_final = week.kmFinal
        week_model.custo = week.custo
        week_model.eficiencia = week.eficiencia
        week_model.litros_abastecidos = week.litrosAbastecidos
        
        self.session.commit()
        
        return self._model_to_entity(week_model)

    def delete(self, week_id: str) -> None:
        week_model = self.session.query(WeekModel).filter(WeekModel.id == week_id).first()
        if week_model:
            self.session.delete(week_model)
            self.session.commit()
    
    def calculate_average_efficiency(self, user_id: str) -> Optional[float]:
        result = self.session.query(
            WeekModel.eficiencia
        ).filter(
            WeekModel.user_id == user_id,
            WeekModel.eficiencia.isnot(None)
        ).all()
        
        if not result:
            return None
        
        total = sum(efficiency[0] for efficiency in result)
        count = len(result)
        return total / count if count > 0 else None
    
    def _model_to_entity(self, model: WeekModel) -> Week:
        return Week(
            id=model.id,
            user_id=model.user_id,
            title=model.title,
            kmAtual=str(model.km_atual),
            kmFinal=str(model.km_final),
            custo=str(model.custo),
            eficiencia=str(model.eficiencia) if model.eficiencia else None,
            litrosAbastecidos=str(model.litros_abastecidos)
        )