from abc import ABC, abstractmethod
from motor.motor_asyncio import AsyncIOMotorGridFSBucket
from fastapi import UploadFile, HTTPException,status
from bson import ObjectId


class ImageUtilsInterface(ABC):

    @abstractmethod
    async def get_image(self, image_id): pass

    @abstractmethod
    async def upload_image(self, filename: str, file: UploadFile): pass

    @abstractmethod
    async def delete_image(self, image_id): pass


class ImageUtils(ImageUtilsInterface):

    def __init__(self, database):
        self._fs = AsyncIOMotorGridFSBucket(database)

    async def _get_chunks(self, grid_out):
        while True:
            chunk = await grid_out.readchunk()
            if not chunk:
                break
            yield chunk


    async def get_image(self, image_id):
        try:
            grid_out = await self._fs.open_download_stream(ObjectId(image_id))
            return self._get_chunks(grid_out=grid_out)
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Image with id {image_id} not found')


    async def upload_image(self, filename: str, file: UploadFile):
        return await self._fs.upload_from_stream(filename, file)

    async def delete_image(self, image_id):
        try:
            await self._fs.delete(ObjectId(image_id))
        except:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f'Image with id {image_id} not found')
