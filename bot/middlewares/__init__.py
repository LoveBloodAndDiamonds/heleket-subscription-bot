__all__ = ["register_middlewares"]

from aiogram import Dispatcher

from .database_middleware import DatabaseMiddleware
from .exceptions_middleware import ExceptionsMiddleware
from .logs_middleware import LogsMiddleware


def register_middlewares(dp: Dispatcher) -> None:
    """
    Register middlewares
    :param dp:
    :return:
    """

    # Register message middlewares
    dp.message.middleware(ExceptionsMiddleware())
    dp.message.middleware(LogsMiddleware())
    dp.message.middleware(DatabaseMiddleware())

    # Register callback middlewares
    dp.callback_query.middleware(ExceptionsMiddleware())
    dp.callback_query.middleware(LogsMiddleware())
    dp.callback_query.middleware(DatabaseMiddleware())
