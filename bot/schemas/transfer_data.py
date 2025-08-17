__all__ = ["TransferData"]

from typing import TypedDict

from aiogram import Bot

from common.database import Database, UserORM


class TransferData(TypedDict):
    """
    This class contains TypedDict structure to store data which will
    transfer throw Dispatcher->Middlewares->Handlers.
    """

    bot: Bot
    db: Database
    user: UserORM
