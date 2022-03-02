from database import currencies_collection


async def get_currencies_collection():
    yield currencies_collection
