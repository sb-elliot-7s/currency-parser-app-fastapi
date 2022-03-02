from datetime import datetime
from fastapi import HTTPException, status
from typing import Optional
from fastapi import UploadFile
from .image_utils import ImageUtilsInterface
from .schemas import GetNewsSchema
from .repositories_interface import RepositoriesInterface
from bson import ObjectId


class Repositories(RepositoriesInterface):

    def __init__(self, collection, image_service: ImageUtilsInterface) -> None:
        self._collection = collection
        self._image_service = image_service

    async def _get_single_news(self, news_id: str) -> dict:
        if not (news := await self._collection.find_one({'_id': news_id})):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'News with id {news_id} not found')
        return news

    async def get_all_news(self, limit: int, skip: int) -> list[GetNewsSchema]:
        return [i async for i in self._collection.find().sort('created', -1).skip(skip).limit(limit)]

    async def get_detail_news(self, news_id: str) -> GetNewsSchema:
        return await self._get_single_news(news_id=ObjectId(news_id))

    async def _upload_images(self, news_id: str, images: Optional[list[UploadFile]]):
        if images:
            for image in images:
                image_id = await self._image_service.upload_image(filename=image.filename, file=image.file)
                await self._collection.update_one({'_id': news_id}, {'$push': {'images': image_id}})

    async def write_news(self, data: dict, images: Optional[list[UploadFile]]):
        data.update({'created': datetime.now()})
        news = await self._collection.insert_one(data)
        await self._upload_images(news_id=news.inserted_id, images=images)
        return await self._get_single_news(news_id=news.inserted_id)

    async def update_news(self, news_id: str, updated_data: dict, images: Optional[list[UploadFile]] = None):
        news = await self._get_single_news(news_id=ObjectId(news_id))
        updated_news = await self._collection.update_one({'_id': news['_id']}, {'$set': updated_data})
        await self._upload_images(news_id=news['_id'], images=images)
        if updated_news:
            return await self.get_detail_news(news_id=news['_id'])

    async def delete_news(self, news_id: str):
        news = await self._get_single_news(news_id=ObjectId(news_id))
        if news.get('images'):
            for image in news['images']:
                await self.delete_image(image_id=image)
        res = await self._collection.delete_one({'_id': news['_id']})
        if res.deleted_count:
            return True

    async def delete_image(self, image_id):
        await self._image_service.delete_image(image_id=image_id)
        news = await self._collection.find_one({'images': {'$in': [ObjectId(image_id)]}})
        await self._collection.update_one({'_id': news['_id']}, {'$pull': {'images': {'$eq': ObjectId(image_id)}}})

    async def get_image(self, image_id):
        return await self._image_service.get_image(image_id=image_id)
