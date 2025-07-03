from sqlalchemy import Column, String, Text, DateTime, ForeignKey, Numeric
from freeroad.infra.database import Base
from datetime import datetime


class WeekModel(Base):
    __tablename__ = "weeks"

    id = Column(String, primary_key=True)
    user_id = Column(String, ForeignKey("users.id"), nullable=False)
    title = Column(String(255), nullable=False)
    km_atual = Column(Numeric(10, 2), nullable=False, comment="Quilometragem atual do veículo")
    km_final = Column(Numeric(10, 2), nullable=False, comment="Quilometragem final do veículo")
    custo = Column(Numeric(10, 2), nullable=False, comment="Custo total do abastecimento")
    eficiencia = Column(Numeric(5, 2), nullable=True, comment="Eficiência em km/l")
    litros_abastecidos = Column(Numeric(8, 3), nullable=False, comment="Quantidade de litros abastecidos")
    created_at = Column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)