from typing import Optional
from .repositories_interface import RepositoriesInterface

from .schemas import CurrencySchema


class Repositories(RepositoriesInterface):

    def __init__(self, collection) -> None:
        self._collection = collection

    async def get_currencies(self, limit: Optional[int] = 10, skip: Optional[int] = 0) -> list[CurrencySchema]:
        return [CurrencySchema(**currency).dict(by_alias=False) async for currency in self._collection.find().skip(skip).limit(limit)]
