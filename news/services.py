from typing import Optional
from fastapi import HTTPException, UploadFile, status
from .repositories_interface import RepositoriesInterface
from .schemas import CreateNewsSchema, UpdateNewsSchema


class NewsServices:
    def __init__(self, repository: RepositoriesInterface) -> None:
        self._repository = repository

    async def get_all_news(self, limit: int, skip: int):
        return await self._repository.get_all_news(limit=limit, skip=skip)

    async def get_detail_news(self, news_id: str):
        return await self._repository.get_detail_news(news_id=news_id)

    async def write_news(self, news_data: CreateNewsSchema, images: Optional[list[UploadFile]] = None):
        return await self._repository.write_news(data=news_data.dict(exclude_none=True), images=images)

    async def update_news(self, news_id: str, updated_data: UpdateNewsSchema, images: Optional[list[UploadFile]] = None):
        return await self._repository.update_news(news_id=news_id, updated_data=updated_data.dict(exclude_none=True), images=images)

    async def delete_news(self, news_id: str):
        if not (result := await self._repository.delete_news(news_id=news_id)):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=f'News with id {news_id} not deleted')

    async def delete_image(self, image_id: str):
        return await self._repository.delete_image(image_id=image_id)

    async def get_image(self, image_id: str):
        return await self._repository.get_image(image_id=image_id)
