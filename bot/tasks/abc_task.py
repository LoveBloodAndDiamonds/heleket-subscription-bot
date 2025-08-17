from abc import ABC, abstractmethod


class ABCTask(ABC):
    """Abstract base class for tasks."""

    @abstractmethod
    async def start(self) -> None: ...

    @abstractmethod
    async def stop(self) -> None: ...
