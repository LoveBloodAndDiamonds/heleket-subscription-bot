__all__ = [
    "register_handlers",
    "bot_commands",
]

from aiogram import Dispatcher

from .commands import bot_commands
from .commands import router as commands_router
from .messages import router as messages_router


def register_handlers(dp: Dispatcher) -> None:
    """Регистрирует обработчики на диспатчер."""
    dp.include_router(commands_router)
    dp.include_router(messages_router)
