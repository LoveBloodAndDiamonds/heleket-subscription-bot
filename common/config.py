"""
Конфигурационные данные и настройка логирования.
"""

__all__ = [
    "config",
    "EnvironmentType",
]

import os
import uuid
from dataclasses import dataclass
from enum import StrEnum
from os import getenv

from aiogram.client.default import DefaultBotProperties
from sqlalchemy import URL


class EnvironmentType(StrEnum):
    """Перечисление типов окружения."""

    DEVELOPMENT = "development"
    PRODUCTION = "production"


@dataclass(frozen=True)
class _DatabaseConfig:
    """Database connection variables."""

    name: str | None = getenv("POSTGRES_DB")
    user: str | None = getenv("POSTGRES_USER")
    passwd: str | None = getenv("POSTGRES_PASSWORD", None)
    port: int = int(getenv("POSTGRES_PORT", "5432"))
    host: str = getenv("POSTGRES_HOST", "db")

    driver: str = "asyncpg"
    database_system: str = "postgresql"

    def build_connection_str(self) -> str:
        """This function build a connection string."""
        return URL.create(
            drivername=f"{self.database_system}+{self.driver}",
            username=self.user,
            database=self.name,
            password=self.passwd,
            port=self.port,
            host=self.host,
        ).render_as_string(hide_password=False)


@dataclass(frozen=True)
class _AdminConfig:
    """Admin panel configuration."""

    title: str = "Subscription Bot"
    """App title"""

    logo_url: str = "https://images.icon-icons.com/3256/PNG/512/admin_lock_padlock_icon_205893.png"
    """Logo url"""

    login: str = getenv("ADMIN_LOGIN", "admin")
    """Admin login"""

    password: str = getenv("ADMIN_PASSWORD", "admin")
    """Admin password"""

    cypher_key: str = getenv("CYPHER_KEY", uuid.UUID(int=uuid.getnode()).hex[-12:])
    """Cypher key"""


@dataclass(frozen=True)
class _BotConfig:
    """Telegram bot configuration."""

    token: str = getenv("BOT_TOKEN", "")
    """Bot token"""

    default_bot_properties = DefaultBotProperties(parse_mode="HTML", link_preview_is_disabled=True)
    """Default bot properties"""


@dataclass(frozen=True)
class _HeleketConfig:
    """Heleket configuration."""

    api_key: str = getenv("HELEKET_API_KEY", "")
    """Heleket API key"""

    merchant_id: str = getenv("HELEKET_MERCHANT_ID", "")
    """Heleket merchant ID"""


@dataclass(frozen=True)
class _BusinessConfig:
    """Business configuration."""

    subscription_price: str = str(getenv("SUBSCRIPTION_PRICE", "15"))
    """Subscription price in dollars"""

    chat_id: int = int(getenv("CHAT_ID", "0"))
    """Chat ID"""

    admin_username: str = getenv("ADMIN_USERNAME", "")
    """Admin username"""


@dataclass(frozen=True)
class Configuration:
    """All in one configuration's class."""

    db: _DatabaseConfig = _DatabaseConfig()
    """Database config"""

    admin: _AdminConfig = _AdminConfig()
    """Admin panel config"""

    bot: _BotConfig = _BotConfig()
    """Telegram bot config"""

    heleket: _HeleketConfig = _HeleketConfig()
    """Heleket config"""

    business: _BusinessConfig = _BusinessConfig()
    """Business config"""

    try:
        environment: EnvironmentType = EnvironmentType(os.getenv("ENVIRONMENT", "production"))
        """Current project environment"""
    except KeyError as err:
        raise ValueError(f"Invalid environment: {os.getenv('ENVIRONMENT')}") from err


config: Configuration = Configuration()
