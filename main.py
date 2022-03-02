from fastapi import FastAPI
from news.controllers import news_router
from currencies.controllers import crypto_router


app = FastAPI(title='Currency App')

app.include_router(news_router)
app.include_router(crypto_router)
