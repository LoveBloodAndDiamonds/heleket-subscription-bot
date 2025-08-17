from typing import Unpack

from aiogram import types

from bot.responses import PROFILE_COMMAND_RESPONSE
from bot.schemas import TransferData


async def profile_command_handler(message: types.Message, **data: Unpack[TransferData]) -> None:
    """/profile command handler"""
    if data["user"].has_subscription:
        subscribtion_status = (
            f"✅ Подписка действительна до: <code>{data['user'].subscription_expires_at}</code>"
        )
    else:
        subscribtion_status = "❌ Подписка неактивна"
    await message.answer(
        PROFILE_COMMAND_RESPONSE.format(
            user_id=message.from_user.id, subscribtion_status=subscribtion_status
        )
    )
