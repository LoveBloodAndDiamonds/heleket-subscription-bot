"""Payment repository file."""

__all__ = ["PaymentRepo"]


from typing import Literal

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import PaymentORM
from .abstract import Repository


class PaymentRepo(Repository[PaymentORM]):
    """Payment repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize payment repository as for all users or only for one user."""
        super().__init__(type_model=PaymentORM, session=session)

    async def create(
        self,
        user_id: int,
        invoice_id: int,
        processed: bool = False,
        status: Literal["paid", "cancelled"] | None = None,
    ) -> PaymentORM:
        """Создание новой записи о платеже."""
        payment = PaymentORM(
            user_id=user_id, invoice_id=invoice_id, processed=processed, status=status
        )

        self.session.add(payment)
        await self.session.flush()  # получаем id без коммита

        return payment
