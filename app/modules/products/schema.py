from typing import Optional, List

from pydantic import BaseModel
from fastapi import Query


class DefaultFilterSchema(BaseModel):
    skip: int = Query(0, ge=0),
    limit: int = Query(10, ge=1, le=100)


class ProductUiInfoSchema(BaseModel):
    price: Optional[float]
    amount: Optional[int]

    class Config:
        orm_mode = True


class ProductSchema(BaseModel):
    id: int
    name: str
    category_id: int
    ui_info: ProductUiInfoSchema

    class Config:
        orm_mode = True


class ProductResponseSchema(ProductSchema):
    id: int

    class Config:
        orm_mode = True


class ProductFilterSchema(DefaultFilterSchema):
    # id: Optional[int] = None
    category_ids: Optional[List[int]] = None
    # name: Optional[str] = None
