from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.config.database.database import get_db
from app.models import ProductsUiInfo
from app.models.orders import Orders
from app.modules.orders.schema import OrderSchema

router = APIRouter()


@router.post("/create")
def create_order(order_data: OrderSchema,db: Session = Depends(get_db)):
    new_order = Orders(
        customer_id=order_data.customer_id,
        product_id=order_data.product_id,
        quantity=order_data.quantity,
        price=order_data.price,
        delivered=order_data.delivered,
        paid=order_data.paid,
    )
    db.add(new_order)
    db.commit()
    db.refresh(new_order)

    product = db.query(ProductsUiInfo).filter(order_data.product_id == ProductsUiInfo.product_id ).first()
    if product:
        product.amount -= order_data.quantity
        db.commit()
        db.refresh(product)

    return new_order


@router.post("/list", response_model=List[OrderSchema])
def get_orders(db: Session = Depends(get_db)):
    return db.query(Orders).all()
