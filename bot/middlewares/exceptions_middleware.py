__all__ = ["ExceptionsMiddleware"]

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from bot.schemas import TransferData
from common.logger import logger


class ExceptionsMiddleware(BaseMiddleware):
    """This middleware handle exceptions"""

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, TransferData], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        """This method calls every update."""
        try:
            return await handler(event, data)
        except Exception as e:
            logger.error(f"Error while handle event: {e}")
            return await data["bot"].send_message(
                chat_id=event.from_user.id,
                text="При обработке Вашего сообщения произошла ошибка.",
            )
