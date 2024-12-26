from pydantic import BaseModel
from fastapi import Query


class DefaultFilterSchema(BaseModel):
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)


class CategorySchema(BaseModel):
    name: str


class CategoryResponseSchema(CategorySchema):
    id: int

    class Config:
        orm_mode = True

