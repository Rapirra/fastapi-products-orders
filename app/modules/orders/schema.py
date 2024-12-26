from enum import Enum

from pydantic import BaseModel


class DeliveryStatus(Enum):
    PENDING = "Pending"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    RETURNED = "Returned"


class OrderSchema(BaseModel):
    customer_id: int
    product_id: int
    quantity: int
    price: float
    paid: bool
    delivered: DeliveryStatus

    class Config:
        use_enum_values = True


class ProductResponseSchema(OrderSchema):
    id: int

    class Config:
        orm_mode = True
