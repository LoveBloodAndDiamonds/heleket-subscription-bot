__all__ = ["DatabaseMiddleware"]

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from bot.schemas import TransferData
from common.database import Database
from common.logger import logger


class DatabaseMiddleware(BaseMiddleware):
    """This middleware throw a Database class to handler."""

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, TransferData], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        """This method calls every update."""
        async with Database.sessionmaker() as session:
            data["db"] = Database(session)

            # Register user if he is not registered
            user = await data["db"].user_repo.get(ident=event.from_user.id)

            if not user:
                logger.info(f"Registering user {event.from_user.id} {event.from_user.full_name}")
                user = await data["db"].user_repo.create(
                    user_id=event.from_user.id,
                    first_name=event.from_user.first_name,
                    last_name=event.from_user.last_name,
                    username=event.from_user.username,
                )
                await data["db"].commit()

            data["user"] = user

            return await handler(event, data)
