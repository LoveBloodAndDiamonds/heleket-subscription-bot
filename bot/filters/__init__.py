__all__ = ["register_filters"]

from aiogram import Dispatcher

from .chat_type_filter import ChatTypeFilter


def register_filters(dp: Dispatcher) -> None:
    """Function setup filters to dispatcher."""
    dp.message.filter(ChatTypeFilter())
    dp.callback_query.filter(ChatTypeFilter())
