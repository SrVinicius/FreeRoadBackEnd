from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Numeric, DateTime
from freeroad.infra.database import Base
from datetime import datetime
from uuid import uuid4


class WeekModel(Base):
    __tablename__ = "weeks"

    id: Mapped[str] = mapped_column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id: Mapped[str] = mapped_column(ForeignKey("users.id"), nullable=False)
    title: Mapped[str] = mapped_column(String(255), nullable=False)
    km_atual: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, comment="Quilometragem atual do veículo")
    km_final: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, comment="Quilometragem final do veículo")
    custo: Mapped[float] = mapped_column(Numeric(10, 2), nullable=False, comment="Custo total do abastecimento")
    eficiencia: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True, comment="Eficiência em km/l")
    litros_abastecidos: Mapped[float] = mapped_column(Numeric(8, 3), nullable=False, comment="Quantidade de litros abastecidos")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)