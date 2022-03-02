from .schemas import CurrencySchema
from .repositories_interface import RepositoriesInterface
from typing import Optional


class CurrenciesService:

    def __init__(self, repository: RepositoriesInterface) -> None:
        self._repository = repository

    async def get_currencies(self, limit: Optional[int] = 10, skip: Optional[int] = 0) -> list[CurrencySchema]:
        return await self._repository.get_currencies(limit=limit, skip=skip)
