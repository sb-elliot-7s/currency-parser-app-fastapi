from database import news_collection


async def get_news_collection():
    yield news_collection
