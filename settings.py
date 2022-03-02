from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):

    mongodb_server: str
    mongodb_port: int
    mongodb_username: str
    mongodb_password: str

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'


@lru_cache
def get_settings() -> Settings:
    return Settings()
