from typing import Optional
from fastapi import APIRouter, File, UploadFile, status, Depends, responses
from .deps import get_news_collection
from .image_utils import ImageUtils
from .repositories import Repositories
from .services import NewsServices
from .schemas import CreateNewsSchema, GetNewsSchema, UpdateNewsSchema
from database import database


news_router = APIRouter(prefix='/news', tags=['news'])


@news_router.get('/', status_code=status.HTTP_200_OK, response_model=list[GetNewsSchema], response_model_by_alias=False)
async def get_all_news(limit: Optional[int] = 10, skip: Optional[int] = 0, news_collection=Depends(get_news_collection)):
    return await NewsServices(repository=Repositories(collection=news_collection, image_service=ImageUtils(database=database)))\
        .get_all_news(limit=limit, skip=skip)


@news_router.get('/{news_id}', status_code=status.HTTP_200_OK, response_model=GetNewsSchema, response_model_by_alias=False)
async def get_detail_news(news_id: str, news_collection=Depends(get_news_collection)):
    return await NewsServices(repository=Repositories(collection=news_collection, image_service=ImageUtils(database=database)))\
        .get_detail_news(news_id=news_id)


@news_router.post('/', status_code=status.HTTP_201_CREATED, response_model=GetNewsSchema, response_model_by_alias=False)
async def write_news(news_collection=Depends(get_news_collection), news_data: CreateNewsSchema = Depends(CreateNewsSchema.as_form),
                     images: Optional[list[UploadFile]] = File(None)):
    return await NewsServices(repository=Repositories(collection=news_collection, image_service=ImageUtils(database=database)))\
        .write_news(news_data=news_data, images=images)


@news_router.put('/{news_id}', status_code=status.HTTP_200_OK, response_model=GetNewsSchema, response_model_by_alias=False)
async def update_news(news_id: str, news_collection=Depends(get_news_collection),
                      updated_data: UpdateNewsSchema = Depends(UpdateNewsSchema.as_form), images: Optional[list[UploadFile]] = File(None)):
    return await NewsServices(repository=Repositories(collection=news_collection, image_service=ImageUtils(database=database)))\
        .update_news(news_id=news_id, updated_data=updated_data, images=images)


@news_router.delete('/{news_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_news(news_id: str, news_collection=Depends(get_news_collection)):
    return await NewsServices(repository=Repositories(collection=news_collection, image_service=ImageUtils(database=database)))\
        .delete_news(news_id=news_id)


@news_router.get('/images/{image_id}', status_code=status.HTTP_200_OK)
async def get_image(image_id: str, news_collection=Depends(get_news_collection)):
    chunk = await NewsServices(repository=Repositories(collection=news_collection, image_service=ImageUtils(database=database))) \
        .get_image(image_id=image_id)
    return responses.StreamingResponse(chunk)


@news_router.delete('/images/{image_id}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_image(image_id: str, news_collection=Depends(get_news_collection)):
    return await NewsServices(repository=Repositories(collection=news_collection, image_service=ImageUtils(database=database)))\
        .delete_image(image_id=image_id)
