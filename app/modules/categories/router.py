from fastapi import Depends, HTTPException, APIRouter
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.config.database.database import get_db
from app.models import Categories
from .schema import CategorySchema, CategoryResponseSchema

router = APIRouter()


@router.post("/create", response_model=CategoryResponseSchema)
def create_product(category_data: CategorySchema, db: Session = Depends(get_db)):
    if not category_data:
        raise HTTPException(status_code=400, detail="product has not been provided")
    try:
        new_category = Categories(
            name=category_data.name,
        )
        db.add(new_category)
        db.commit()
        db.refresh(new_category)

        return new_category

    except SQLAlchemyError as e:
        db.rollback()
        raise RuntimeError(f"Failed to create product: {e}")
