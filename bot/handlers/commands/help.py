from aiogram import types

from bot.responses import HELP_COMMAND_RESPONSE


async def help_command_handler(message: types.Message) -> None:
    """/help command handler"""
    await message.answer(HELP_COMMAND_RESPONSE)
