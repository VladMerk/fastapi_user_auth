from sqlalchemy.orm import Mapped, mapped_column

from core.database import Base


class Users(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(unique=True)
    password: Mapped[str] = mapped_column()
    is_active: Mapped[bool] = mapped_column(server_default="TRUE", default=True)
