__all__ = ["CheckInvoiceTask"]


import asyncio
import base64
import hashlib
import json
from datetime import datetime, timedelta
from typing import Any

import aiohttp
from aiogram import Bot

from bot.responses import SUCCESSFUL_SUBSCRIPTION_RESPONSE
from common.config import config
from common.database import Database, PaymentORM
from common.logger import logger

from .abc_task import ABCTask


class CheckInvoiceTask(ABCTask):
    """Check invoice task.
    Create and send invite link to channel if invoice was paid."""

    def __init__(self, bot: Bot, session: aiohttp.ClientSession | None = None) -> None:
        self._bot = bot
        self._running = False
        self._session = session or aiohttp.ClientSession()

    async def start(self) -> None:
        self._running = True
        while self._running:
            try:
                async with Database.sessionmaker() as session:
                    database = Database(session)
                    invoices = await database.payment_repo.get_many(
                        whereclause=PaymentORM.processed == False  # noqa
                    )
                    for invoice in invoices:
                        try:
                            await self._process_invoice(database, invoice)
                        except Exception as e:
                            logger.error(f"Error while processing invoice: {e}")
                        await asyncio.sleep(1)
                    # Сохраняем изменения в базе данных
                    await database.commit()
            except Exception as e:
                logger.error(f"Error while checking invoice: {e}")
            await asyncio.sleep(10)

    async def _process_invoice(self, database: Database, invoice: PaymentORM) -> None:
        invoice_info = await self._fetch_invoice_info(order_id=invoice.invoice_id)
        logger.debug(f"invoice_info: {invoice_info}")
        invoice_status = invoice_info["result"]["status"]

        if invoice_status in ["fail", "cancel", "system_fail"]:
            invoice.processed = True
            invoice.status = "cancelled"
            await database.commit()
            return

        if invoice_status in ["paid", "paid_over"]:
            logger.success(f"Invoice {invoice.id} processed successfully")
            # Выдаем подписку пользователю
            user = await database.user_repo.get(ident=invoice.user_id)
            if not user:
                logger.error(f"User not found for invoice {invoice.id}")
                return
            if user.subscription_expires_at > datetime.now():
                new_expire_date = user.subscription_expires_at + timedelta(days=31)
            else:
                new_expire_date = datetime.now() + timedelta(days=31)
            user.subscription_expires_at = new_expire_date

            # Обновляем статус платежа
            invoice.processed = True

            # Отправляем сообщение пользователю
            invite_link = await self._bot.create_chat_invite_link(
                chat_id=config.business.chat_id,
                expire_date=None,
                member_limit=1,
            )
            await self._bot.send_message(
                chat_id=invoice.user_id,
                text=SUCCESSFUL_SUBSCRIPTION_RESPONSE.format(
                    subscription_expire_date=new_expire_date, invite_link=invite_link.invite_link
                ),
            )
            return

    @staticmethod
    def _generate_signature(data: str, api_key: str) -> str:
        """Generates sign for heleket.com"""
        return hashlib.md5(
            base64.b64encode(data.encode("ascii")) + api_key.encode("ascii")
        ).hexdigest()

    @staticmethod
    def _generate_headers(signature: str, merchant_id: str) -> dict[str, Any]:
        """Generates headers for heleket.com"""
        return {"merchant": merchant_id, "sign": signature, "Content-Type": "application/json"}

    async def _fetch_invoice_info(self, order_id: str) -> dict[str, Any]:
        """Creates invoice for heleket.com"""
        payment_info = json.dumps({"order_id": order_id})
        signature = self._generate_signature(payment_info, config.heleket.api_key)
        headers = self._generate_headers(signature, config.heleket.merchant_id)
        async with self._session.post(
            "https://api.heleket.com/v1/payment/info",
            headers=headers,
            data=payment_info,
        ) as resp:
            resp.raise_for_status()
            return await resp.json()

    async def stop(self) -> None:
        self._running = False
        await self._session.close()
