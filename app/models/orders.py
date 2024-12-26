from sqlalchemy import Column, Integer, Boolean, ForeignKey, Enum, Float
from app.config.database.database import Base

from enum import Enum as PyEnum


class DeliveryStatus(PyEnum):
    PENDING = "Pending"
    IN_TRANSIT = "In Transit"
    DELIVERED = "Delivered"
    RETURNED = "Returned"


class Orders(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    customer_id = Column(Integer, ForeignKey('users.id'))
    product_id = Column(Integer, ForeignKey('products.id'))
    quantity = Column(Integer)
    price = Column(Float)
    paid = Column(Boolean, default=False)
    delivered = Column(Enum(DeliveryStatus), default=DeliveryStatus.PENDING)
