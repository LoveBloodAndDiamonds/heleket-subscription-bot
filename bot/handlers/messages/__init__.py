__all__ = [
    "router",
]

from aiogram import Router

from .unhandled import unhandled_callbacks, unhandled_messages

router = Router(name="message_router")

router.callback_query.register(unhandled_callbacks)
router.message.register(unhandled_messages)
