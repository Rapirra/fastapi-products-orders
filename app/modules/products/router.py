from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config.database.database import get_db
from app.config.jwt.security import verify_token
from app.models import Products, ProductsUiInfo
from .schema import ProductSchema


router = APIRouter()


@router.post("/create")
def create_product(product_data: ProductSchema, db: Session = Depends(get_db)):
    if not product_data:
        raise HTTPException(status_code=400, detail="product has not been provided")
    try:
        new_product = Products(
            name=product_data.name,
            category_id=product_data.category_id
        )
        db.add(new_product)
        db.flush()

        product_ui_info = ProductsUiInfo(
            product_id=new_product.id,
            price=product_data.price,
            amount=product_data.amount
        )
        db.add(product_ui_info)

        db.commit()

        db.refresh(new_product)
        db.refresh(product_ui_info)

        return new_product, product_ui_info

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Failed to create product: {e}")


@router.get("/list",  response_model=List[ProductSchema])
def get_products(token: str,  db: Session = Depends(get_db)):
    username = verify_token(token)
    print('get_products', username)
    return db.query(Products).all()
    # query = db.query(Products)

    # if products_filter.id:
    #     query = query.filter_by(id=products_filter.id)
    #
    # if products_filter.category_ids:
    #     query = query.filter(Products.category_id.in_(products_filter.category_ids))
    #
    # if products_filter.name:
    #     query = query.filter(Products.name.ilike(f"%{products_filter.name}%"))
    #
    # products = query.all()
    #
    # if not products:
    #     raise HTTPException(status_code=404, detail="No products found")




