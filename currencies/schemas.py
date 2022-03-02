from typing import Optional
from pydantic import BaseModel, Field

from news.schemas import ObjID


class CurrencySchema(BaseModel):
    id: ObjID = Field(alias='_id')
    rank: int
    name: str
    symbol: str = Field(..., max_length=10)
    market_cap: str
    price: str 
    change_in_procent_24H: Optional[str]


    class Config:
        json_encoders = {ObjID: lambda x: str(x)}
