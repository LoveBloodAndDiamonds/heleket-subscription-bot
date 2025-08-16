"""
Configuration file.
"""

__all__ = [
    "logger",
    "get_logger",
]

import sys
from pathlib import Path
from typing import TYPE_CHECKING, Literal

from loguru import logger

if TYPE_CHECKING:
    from loguru import Logger


class LoggerFactory:
    """Factory for creating and caching loggers."""

    # Remove default loguru handlers
    logger.remove()

    # Define retentions for each level
    _retentions: dict[str, str] = {
        "ERROR": "1 month",
        "INFO": "1 week",
        "DEBUG": "1 day",
        "TRACE": "3 hours",
    }

    # Loggers stash
    _loggers: dict[str, "Logger"] = {}

    @classmethod
    def get_logger(
        cls,
        name: str = "",
        base_dir: str = "logs",
        stdout_level: Literal["ERROR", "INFO", "DEBUG", "TRACE"] = "DEBUG",
        file_levels: list[Literal["ERROR", "INFO", "DEBUG", "TRACE"]] | None = None,
        enqueue: bool = False,
    ) -> "Logger":
        """
        Returns an existing logger or creates a new one.

        :param name: Logger name (used for file storage).
        :param base_dir: Base directory for log files.
        :param stdout_level: Logging level for console output.
        :param file_levels: Levels for file output. Default: ["ERROR", "INFO", "DEBUG"]
        :param enqueue: Enables async logging (recommended for high-load apps).
        :return: Logger instance.
        """
        if name in cls._loggers:
            return cls._loggers[name]  # Return cached logger

        log_path = Path(base_dir) / name
        log_path.mkdir(parents=True, exist_ok=True)

        log = logger.bind(name=name)

        # Console logging
        log.add(
            sys.stderr,
            level=stdout_level,
            filter=lambda record: name == record["extra"].get("name"),
            format=(
                "<white>{time: %d.%m %H:%M:%S}</white>|"
                "<level>{level}</level>|"
                "{extra[name]}|"
                "<bold>{message}</bold>"
            )
            if name
            else (
                "<white>{time: %d.%m %H:%M:%S}</white>|"
                "<level>{level}</level>|"
                "<bold>{message}</bold>"
            ),
        )

        # File logging for different levels
        for level in file_levels or ["ERROR", "INFO", "DEBUG"]:
            log.add(
                sink=log_path / f"{level.lower()}.log",  # Path for log file
                filter=lambda record: name == record["extra"].get("name"),
                level=level,
                format=(
                    "<white>{time: %d.%m %H:%M:%S.%f}</white> | "
                    "<level>{level}</level>| "
                    "{extra[name]}|"
                    "{name} {function} line:{line}| "
                    "<bold>{message}</bold>"
                )
                if name
                else (
                    "<white>{time: %d.%m %H:%M:%S.%f}</white> | "
                    "<level>{level}</level>| "
                    "{name} {function} line:{line}| "
                    "<bold>{message}</bold>"
                ),
                retention=cls._retentions.get(level, "1 week"),
                rotation="10 MB",
                compression="zip",
                encoding="utf-8",
                enqueue=enqueue,
            )

        cls._loggers[name] = log  # Cache the logger
        return log


get_logger = LoggerFactory.get_logger  # Shortcut for convenience

logger = get_logger()  # Base logger
