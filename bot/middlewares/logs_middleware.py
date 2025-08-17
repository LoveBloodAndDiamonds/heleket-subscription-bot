__all__ = ["LogsMiddleware"]

from collections.abc import Awaitable, Callable
from typing import Any

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery, Message

from bot.schemas import TransferData
from common.logger import logger


class LogsMiddleware(BaseMiddleware):
    """This middleware logs users actions"""

    async def __call__(
        self,
        handler: Callable[[Message | CallbackQuery, TransferData], Awaitable[Any]],
        event: Message | CallbackQuery,
        data: TransferData,
    ) -> Any:
        """This method calls every update."""
        try:
            if isinstance(event, Message):
                event_type = "Message"
                event_data = event.text
            elif isinstance(event, CallbackQuery):
                event_type = "Callback"
                event_data = event.data
            else:
                event_type = type(event)
                event_data = "Unknown"
            logger.debug(f"{event_type} from {event.from_user.id}: {event_data}")

            return await handler(event, data)
        except Exception as e:
            logger.exception(f"Error handling event: {e}")
