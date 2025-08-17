__all__ = ["CheckSubscriptionTask"]

import asyncio

from aiogram import Bot

from bot.responses import SUBSCRIPTION_EXPIRED_RESPONSE
from common.config import config
from common.database import Database, UserORM
from common.logger import logger

from .abc_task import ABCTask


class CheckSubscriptionTask(ABCTask):
    """Check subscription task.
    Deletes user from channel if subscription is expired."""

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._running = False

    async def start(self) -> None:
        self._running = True
        while self._running:
            try:
                async with Database.sessionmaker() as session:
                    database = Database(session)
                    users = await database.user_repo.get_many(
                        whereclause=UserORM.banned == False  # noqa
                    )
                    for user in users:
                        await self._process_user(database, user)
            except Exception as e:
                logger.error(f"Error while checking subscription: {e}")
            await asyncio.sleep(60)

    async def _process_user(self, database: Database, user: UserORM) -> None:
        if user.has_subscription:
            return
        logger.info(f"User {user.user_id} has no subscription")
        await self._bot.ban_chat_member(chat_id=config.business.chat_id, user_id=user.user_id)
        await self._bot.unban_chat_member(chat_id=config.business.chat_id, user_id=user.user_id)
        user.banned = True
        await database.commit()

        await self._bot.send_message(chat_id=user.user_id, text=SUBSCRIPTION_EXPIRED_RESPONSE)

    async def stop(self) -> None:
        self._running = False
