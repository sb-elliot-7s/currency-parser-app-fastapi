from abc import ABC, abstractmethod
from typing import Optional
from .schemas import CurrencySchema


class RepositoriesInterface(ABC):

    @abstractmethod
    async def get_currencies(self, limit: Optional[int] = 10, skip: Optional[int] = 0) -> list[CurrencySchema]: pass
