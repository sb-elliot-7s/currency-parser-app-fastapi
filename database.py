from settings import get_settings

import motor.motor_asyncio

_mongodb = f'mongodb://{get_settings().mongodb_username}:{get_settings().mongodb_password}@{get_settings().mongodb_server}:{get_settings().mongodb_port}'


client = motor.motor_asyncio.AsyncIOMotorClient(_mongodb)
database = client.db

news_collection = database.news
currencies_collection = database.currencies
