from typing import Optional
from fastapi import APIRouter, Depends, WebSocket, WebSocketDisconnect
from .deps import get_currencies_collection
from .services import CurrenciesService
from .repositories import Repositories
import asyncio

crypto_router = APIRouter(prefix='/crypto')


@crypto_router.websocket("/")
async def get_currencies(websocket: WebSocket, limit: Optional[int] = 10, skip: Optional[int] = 0,
                         currencies_collection=Depends(get_currencies_collection)):
    await websocket.accept()
    while True:
        currencies = await CurrenciesService(repository=Repositories(collection=currencies_collection)) \
            .get_currencies(limit=limit, skip=skip)
        try:
            await websocket.send_json(data=currencies)
            await asyncio.sleep(300)
        except WebSocketDisconnect:
            await websocket.close()
