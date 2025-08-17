from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware import Middleware
from starlette.middleware.sessions import SessionMiddleware
from starlette_admin import CustomView
from starlette_admin.contrib.sqla import Admin

from common.config import EnvironmentType, config
from common.database import Database, PaymentORM, UserORM
from common.logger import logger

from .auth import AdminAuthProvider
from .view import LogsCustomView, MetrCustomView, PaymentModelView, UserModelView


def register_admin_routes(app: FastAPI) -> None:
    """Function register admin views to fastApi appliaction."""

    # Init starlette-admin instance
    admin = Admin(
        engine=Database.engine,
        login_logo_url=config.admin.logo_url,
        auth_provider=AdminAuthProvider(),
        base_url="/admin",
        templates_dir="app/templates",
        middlewares=[Middleware(SessionMiddleware, secret_key=config.admin.cypher_key)],
    )

    # Add views
    admin.add_view(CustomView(label="Инструкция", icon="fa fa-info"))
    admin.add_view(UserModelView(model=UserORM, label="Пользователи", icon="fa fa-user"))
    admin.add_view(
        PaymentModelView(model=PaymentORM, label="Платежи", icon="fa fa-credit-card-alt")
    )
    admin.add_view(LogsCustomView(label="Логи", path="/logs", icon="fa fa-book"))
    admin.add_view(MetrCustomView(label="Система", path="/monitoring", icon="fa fa-heartbeat"))

    # Mount starlette-admin instance to fastApi applaction
    admin.mount_to(app)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Управление жизненным циклом приложения."""
    # Launch logs
    logger.info(f"Admin panel startup! Environment: {config.environment}")
    if config.environment == EnvironmentType.DEVELOPMENT:
        logger.debug("Admin panel url: http://127.0.0.1:8000/admin")
    else:
        logger.info("App started!")

    # Register admin routes
    register_admin_routes(app)

    # Give control to FastAPI
    yield

    # Shutdown logs
    logger.info("Admin panel shutdown!")


# Main FastAPI object
app = FastAPI(
    lifespan=lifespan,
    **{
        "docs_url": None,
        "redoc_url": None,
        "openapi_url": None,
    }
    if config.environment == EnvironmentType.PRODUCTION
    else {},  # type: ignore
)
