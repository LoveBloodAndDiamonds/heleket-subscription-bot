__all__ = [
    "router",
    "bot_commands",
]

from aiogram import Router
from aiogram.filters import Command, CommandStart
from aiogram.types import BotCommand

from .contacts import contacts_command_handler
from .help import help_command_handler
from .profile import profile_command_handler
from .start import start_command_handler
from .subscribe import subscribe_command_handler

router = Router(name="command_router")
router.message.register(start_command_handler, CommandStart())
router.message.register(help_command_handler, Command("help"))
router.message.register(contacts_command_handler, Command("contacts"))
router.message.register(subscribe_command_handler, Command("subscribe"))
router.message.register(profile_command_handler, Command("profile"))

bot_commands = [
    BotCommand(command="help", description="Список доступных комманд"),
    BotCommand(command="subscribe", description="Оплатить подписку"),
    BotCommand(command="profile", description="Профиль пользователя"),
    BotCommand(command="contacts", description="Контакты для связи"),
]
