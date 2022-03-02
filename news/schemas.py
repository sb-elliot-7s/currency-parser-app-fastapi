
from datetime import datetime
from typing import Optional
from fastapi import Form
from pydantic import BaseModel, Field
from bson import ObjectId


class ObjID(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, ObjectId):
            raise TypeError('ObjectId required')
        return str(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")


class CreateNewsSchema(BaseModel):
    title: str = Field(..., max_length=500)
    description: str

    @classmethod
    def as_form(cls, title: str = Form(...), description: str = Form(...)):
        return cls(title=title, description=description)


class UpdateNewsSchema(BaseModel):
    title: Optional[str] = Field(None, max_length=500)
    description: Optional[str]

    @classmethod
    def as_form(cls, title: Optional[str] = Form(None), description: Optional[str] = Form(None)):
        return cls(title=title, description=description)


class GetNewsSchema(CreateNewsSchema):
    id: ObjID = Field(alias='_id')
    created: datetime
    images: Optional[list[ObjID]]

    class Config:
        json_encoders = {
            ObjID: lambda v: str(v),
            datetime: lambda v: v.strftime('%Y:%m:%d %H:%M')
        }
