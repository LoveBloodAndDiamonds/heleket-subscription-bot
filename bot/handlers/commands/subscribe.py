import base64
import hashlib
import json
from typing import Any, Unpack
from uuid import uuid4

from aiogram import types
from aiohttp import ClientSession

from bot.responses import SUBSCRIBE_COMMAND_RESPONSE
from bot.schemas import TransferData
from common.config import config
from common.logger import logger


def _generate_signature(data: str, api_key: str) -> str:
    """Generates sign for heleket.com"""
    return hashlib.md5(base64.b64encode(data.encode("ascii")) + api_key.encode("ascii")).hexdigest()


def _generate_headers(signature: str, merchant_id: str) -> dict[str, Any]:
    """Generates headers for heleket.com"""
    return {"merchant": merchant_id, "sign": signature, "Content-Type": "application/json"}


async def _create_invoice(order_id: str) -> dict[str, Any]:
    """Creates invoice for heleket.com"""
    async with ClientSession() as session:
        payment_data = json.dumps(
            {
                "amount": config.business.subscription_price,
                "currency": "USDT",
                "order_id": order_id,
            }
        )
        signature = _generate_signature(payment_data, config.heleket.api_key)
        headers = _generate_headers(signature, config.heleket.merchant_id)
        response = await session.post(
            "https://api.heleket.com/v1/payment",
            headers=headers,
            data=payment_data,
        )
        response.raise_for_status()
        return await response.json()


async def subscribe_command_handler(message: types.Message, **data: Unpack[TransferData]) -> None:
    """/subscribe command handler"""
    try:
        order_id = str(uuid4())
        invoice = await _create_invoice(order_id)

        # Записываем данные о созданном платеже в базу данных
        invoice_id = invoice["result"]["order_id"]
        await data["db"].payment_repo.create(
            user_id=message.from_user.id,
            invoice_id=invoice_id,
        )
        data["user"].banned = False  # Отмечаем пользователя активным
        await data["db"].commit()

        # Отправляем пользователю клавиатуру с сылкой и текст
        invoice_link = invoice["result"]["url"]
        keyboard = types.InlineKeyboardMarkup(
            inline_keyboard=[
                [types.InlineKeyboardButton(text="💳 Оплатить", url=invoice_link)],
            ]
        )

        await message.answer(
            SUBSCRIBE_COMMAND_RESPONSE.format(
                subscription_price=config.business.subscription_price
            ),
            reply_markup=keyboard,
        )
    except Exception as e:
        logger.error(f"Error creating invoice: {e}")
        await message.answer("‼️ Ошибка при создании ссылки на оплату. Попробуйте позже.")
        return
