from abc import ABC, abstractmethod
from typing import Optional
from fastapi import UploadFile


class RepositoriesInterface(ABC):

    @abstractmethod
    async def get_all_news(self, limit: int, skip: int): pass

    @abstractmethod
    async def get_detail_news(self, news_id: str): pass

    @abstractmethod
    async def write_news(self, data: dict, images: Optional[list[UploadFile]] = None): pass

    @abstractmethod
    async def update_news(self, news_id: str, updated_data: dict,images: Optional[list[UploadFile]] = None): pass

    @abstractmethod
    async def delete_news(self, news_id: str): pass

    @abstractmethod
    async def delete_image(self, image_id): pass

    @abstractmethod
    async def get_image(self, image_id): pass
