from datetime import UTC, datetime

from sqlalchemy import BigInteger
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base, created_at
from .payment import PaymentORM


class UserORM(Base):
    """Модель пользователя."""

    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    """Телеграм юзер айди"""

    first_name: Mapped[str | None]
    """Имя пользователя из телеграм"""

    last_name: Mapped[str | None]
    """Фамилия пользователя из телеграм"""

    username: Mapped[str | None]
    """Юзернейм пользователя из телеграм"""

    subscription_expires_at: Mapped[created_at]
    """Дата и время истечения подписки"""

    banned: Mapped[bool]
    """Забанен ли пользователь"""

    # === Relationships === #

    payments: Mapped[list[PaymentORM]] = relationship("PaymentORM", back_populates="user")
    """Связь с транзакциями пользователя"""

    @property
    def has_subscription(self) -> bool:
        return self.subscription_expires_at > datetime.now(UTC).replace(tzinfo=None)

    def __str__(self) -> str:
        return f"User {self.user_id} {self.first_name}"

    def __repr__(self) -> str:
        return f"<User {self.user_id} {self.first_name}>"

    # Starlette-admin representations
    # Docs: https://jowilf.github.io/starlette-admin/user-guide/configurations/modelview/

    def __admin_repr__(self, *_, **__) -> str:
        return f"[User {self.user_id} {self.first_name}]"

    def __admin_select2_repr__(self, *_, **__) -> str:
        return f"<span>User {self.user_id} {self.first_name}</span>"
