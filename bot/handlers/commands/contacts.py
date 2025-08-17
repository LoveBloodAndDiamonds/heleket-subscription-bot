from aiogram import types

from bot.responses import CONTACTS_COMMAND_RESPONSE
from common.config import config


async def contacts_command_handler(message: types.Message) -> None:
    """/contacts command handler"""
    await message.answer(
        CONTACTS_COMMAND_RESPONSE.format(admin_username=config.business.admin_username)
    )
