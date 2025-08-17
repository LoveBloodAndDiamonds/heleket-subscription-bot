__all__ = ["TaskManager"]


import asyncio

from aiogram import Bot

from .abc_task import ABCTask
from .check_invoice import CheckInvoiceTask
from .check_subscription import CheckSubscriptionTask


class TaskManager:
    """Tasks manager."""

    def __init__(self, bot: Bot) -> None:
        self._bot = bot
        self._tasks: list[ABCTask] = []

    async def at_startup(self) -> None:
        """Start tasks."""
        self._tasks.append(CheckInvoiceTask(bot=self._bot))
        self._tasks.append(CheckSubscriptionTask(bot=self._bot))
        await asyncio.gather(*[t.start() for t in self._tasks])

    async def at_shutdown(self) -> None:
        """Stop tasks."""
        await asyncio.gather(*[t.stop() for t in self._tasks])
