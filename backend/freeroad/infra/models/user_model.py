from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Column
from freeroad.infra.database import Base
from freeroad.domain.entities.user import User
from freeroad.domain.value_objects.email_vo import Email
from freeroad.domain.value_objects.password import Password


class UserModel(Base):
    __tablename__ = "users"

    id: Mapped[str] = mapped_column(String, primary_key=True, index=True)
    name: Mapped[str] = mapped_column(String, nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    password: Mapped[str] = mapped_column(String, nullable=False)
    role: Mapped[str] = mapped_column(String, nullable=False)

    def to_entity(self) -> User:
        """
        Converte o modelo SQLAlchemy para uma entidade de domínio.
        """
        return User(
            id=self.id,
            name=self.name,
            email=Email(self.email),
            password=Password(self.password, hashed=True),
            role=self.role,
        )
