from abc import ABC, abstractmethod
from typing import Any


class RelationalDB(ABC):
    """Abstract base class for relational databases."""

    @abstractmethod
    def get(self, *args, **kwargs): ...

    @abstractmethod
    def create(self, *args, **kwargs): ...

    @abstractmethod
    def update(self, *args, **kwargs): ...

    @abstractmethod
    def delete(self, *args, **kwargs): ...
