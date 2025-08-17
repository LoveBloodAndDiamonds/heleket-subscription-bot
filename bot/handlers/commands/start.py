from typing import Unpack

from aiogram import types

from bot.responses import START_COMMAND_RESPONSE
from bot.schemas import TransferData


async def start_command_handler(message: types.Message, **data: Unpack[TransferData]) -> None:
    """/start command handler"""
    await message.answer(START_COMMAND_RESPONSE.format(user=message.from_user.full_name))
