"""User repository file."""

__all__ = ["UserRepo"]

import datetime

from sqlalchemy.ext.asyncio import AsyncSession

from ..models import UserORM
from .abstract import Repository


class UserRepo(Repository[UserORM]):
    """User repository for CRUD and other SQL queries."""

    def __init__(self, session: AsyncSession):
        """Initialize user repository as for all users or only for one user."""
        super().__init__(type_model=UserORM, session=session)

    async def create(
        self,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        username: str | None = None,
        subscription_expires_at: datetime.datetime | None = None,
        banned: bool = True,
    ) -> UserORM:
        """Create a new user in the database."""
        # Создаем новый экземпляр UserORM
        new_user = UserORM(
            user_id=user_id,
            first_name=first_name,
            last_name=last_name,
            username=username,
            subscription_expires_at=subscription_expires_at,
            banned=banned,
        )

        # Добавляем его в сессию
        self.session.add(new_user)

        return new_user

    async def update(
        self,
        user_id: int,
        first_name: str | None = None,
        last_name: str | None = None,
        username: str | None = None,
        subscription_expires_at: datetime.datetime | None = None,
    ) -> UserORM | None:
        """Update an existing user in the database."""
        # Получаем пользователя по user_id
        user = await self.get(user_id)

        if not user:
            # Если пользователь не найден, возвращаем None
            return None

        # Обновляем только те поля, которые были переданы
        if first_name is not None:
            user.first_name = first_name
        if last_name is not None:
            user.last_name = last_name
        if username is not None:
            user.username = username
        if subscription_expires_at is not None:
            user.subscription_expires_at = subscription_expires_at

        return user
