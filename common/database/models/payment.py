from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base

if TYPE_CHECKING:
    from .user import UserORM


class PaymentORM(Base):
    """Модель транзакции пользователя."""

    __tablename__ = "payments"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    """Первичный ключ транзакции"""

    user_id: Mapped[int] = mapped_column(ForeignKey("users.user_id"), nullable=False)
    """Внешний ключ на пользователя (user_id из таблицы пользователей)"""

    user: Mapped["UserORM"] = relationship("UserORM", back_populates="payments")
    """Связь с моделью пользователя"""

    invoice_id: Mapped[str]
    """Айди платежа у провайдера"""

    processed: Mapped[bool] = mapped_column(default=False)
    """Статус подписки"""

    status: Mapped[str] = mapped_column(nullable=True)
    """Статус платежа"""

    def __str__(self):
        return f"Payment#{self.id} from {self.user_id}"

    def __repr__(self):
        return f"<Payment#{self.id} from {self.user_id}>"

    # Starlette-admin representations
    # Docs: https://jowilf.github.io/starlette-admin/user-guide/configurations/modelview/

    def __admin_repr__(self, *_, **__) -> str:
        return f"[Payment#{self.id}]"

    def __admin_select2_repr__(self, *_, **__) -> str:
        return f"<span>Payment#{self.id} from {self.user_id}</span>"
