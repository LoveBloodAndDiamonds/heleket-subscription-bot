__all__ = [
    "ChatTypeFilter",
]


from aiogram.filters import BaseFilter
from aiogram.types import CallbackQuery, Message


class ChatTypeFilter(BaseFilter):
    """Фильтр на типы чаты."""

    def __init__(self, chat_type: str = "private"):
        self.chat_type = chat_type

    async def __call__(self, event: Message | CallbackQuery) -> bool:
        if isinstance(event, Message):
            return event.chat.type == self.chat_type
        elif isinstance(event, CallbackQuery):
            return event.message.chat.type == self.chat_type
