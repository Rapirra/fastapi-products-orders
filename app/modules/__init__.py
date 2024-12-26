from fastapi import APIRouter
from app.modules.auth.router import router as auth_router
from app.modules.user.router import router as user_router
from app.modules.products.router import router as products_router
from app.modules.orders.router import router as orders_router
from app.modules.categories.router import router as categories_router

router = APIRouter()
router.include_router(auth_router, prefix="/auth", tags=["Auth"])
router.include_router(user_router, prefix="/user", tags=["User"])
router.include_router(orders_router, prefix="/orders", tags=["Orders"])
router.include_router(products_router, prefix="/products", tags=["Products"])
router.include_router(categories_router, prefix="/categories", tags=["Categories"])