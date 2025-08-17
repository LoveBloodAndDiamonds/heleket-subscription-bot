from aiogram import types

from bot.responses import UNHANDLED_MESSAGE_RESPONSE
from common.logger import logger


async def unhandled_messages(message: types.Message):
    """unhandled messages"""
    logger.debug(
        f"Unhandled message from {message.from_user.id}, {message.chat.id}: {message.text}"
    )
    await message.answer(UNHANDLED_MESSAGE_RESPONSE)


async def unhandled_callbacks(callback: types.CallbackQuery):
    """unhandled callbacks"""
    logger.debug(
        f"Unhandled message from {callback.from_user.id}, {callback.message.chat.id}: {callback.data}"
    )
    await callback.answer(UNHANDLED_MESSAGE_RESPONSE)
