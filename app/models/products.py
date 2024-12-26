from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship

from app.config.database.database import Base


class Categories(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    products = relationship("Products", back_populates="category")


class Products(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey("categories.id"))
    category = relationship("Categories", back_populates="products")
    ui_info = relationship("ProductsUiInfo", back_populates="product", uselist=False)


class ProductsUiInfo(Base):
    __tablename__ = "productsUiInfo"
    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"))
    price = Column(Float)
    amount = Column(Integer)
    product = relationship("Products", back_populates="ui_info")
