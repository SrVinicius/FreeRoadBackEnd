from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Numeric, DateTime
from freeroad.infra.database import Base
from datetime import datetime
from uuid import uuid4
from freeroad.domain.entities.week import Week


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
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now)
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.now, onupdate=datetime.now)
    
    # Relacionamentos
    user = relationship("UserModel", back_populates="weeks")

    def to_entity(self) -> Week:
        """Converte o modelo para uma entidade de domínio"""
        return Week(
            id=self.id,
            user_id=self.user_id,
            title=self.title,
            kmAtual=str(self.km_atual),
            kmFinal=str(self.km_final),
            custo=str(self.custo),
            eficiencia=str(self.eficiencia) if self.eficiencia is not None else "0",
            litrosAbastecidos=str(self.litros_abastecidos),
        )
    
    @classmethod
    def from_entity(cls, week: Week) -> "WeekModel":
        """Cria um modelo a partir de uma entidade de domínio"""
        return cls(
            id=week.id,
            user_id=week.user_id,
            title=week.title,
            km_atual=float(week.kmAtual),
            km_final=float(week.kmFinal) if week.kmFinal else 0.0,
            custo=float(week.custo),
            eficiencia=float(week.eficiencia) if week.eficiencia and week.eficiencia != "0" else None,
            litros_abastecidos=float(week.litrosAbastecidos),
        )