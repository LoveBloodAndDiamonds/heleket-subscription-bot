from aiogram import types

from bot.responses import START_COMMAND_RESPONSE


async def start_command_handler(message: types.Message) -> None:
    """/start command handler"""
    await message.answer(START_COMMAND_RESPONSE.format(user=message.from_user.full_name))
