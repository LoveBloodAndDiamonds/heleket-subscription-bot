import asyncio

from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage

from common.config import config
from common.logger import logger

from .filters import register_filters
from .handlers import bot_commands, register_handlers
from .middlewares import register_middlewares
from .tasks import TaskManager


async def start_bot():
    """Функция запускает бота."""
    try:
        bot = Bot(
            token=config.bot.token,
            default=config.bot.default_bot_properties,
        )

        # Dispatcher
        dp = Dispatcher(storage=MemoryStorage())

        # Handlers registration
        register_handlers(dp)

        # Middlewares registration
        register_middlewares(dp)

        # Filters registration
        register_filters(dp)

        # Register commands
        await bot.set_my_commands(commands=bot_commands)

        # Task manager initialization
        task_manager = TaskManager(bot=bot)
        asyncio.create_task(task_manager.at_startup())

        # Log startup
        logger.warning(f"Bot @{(await bot.get_me()).username} started up!")

        # Launch polling
        await dp.start_polling(
            bot, allowed_updates=dp.resolve_used_update_types(), skip_updates=True
        )
    except KeyboardInterrupt:
        logger.warning("KeyboardInterrupt")
    except Exception as e:
        logger.error(f"Error ({type(e)}) while starting bot: {e}")
    finally:
        logger.info("Bot shutdown")
        try:
            await asyncio.gather(bot.session.close(), task_manager.at_shutdown())
        except Exception as e:
            logger.error(f"Error ({type(e)}) while shutting down bot: {e}")


if __name__ == "__main__":
    asyncio.run(start_bot())
