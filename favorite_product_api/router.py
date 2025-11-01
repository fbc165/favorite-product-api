from fastapi import APIRouter

from favorite_product_api.auth.auth import jwt_bearer
from favorite_product_api.auth.routes import router as auth_router
from favorite_product_api.user_favorite_products.routes import (
    router as user_favorite_products_router,
)
from favorite_product_api.users.routes import router as users_router

api_v1_router = APIRouter()

api_v1_router.include_router(users_router, prefix="/users", tags=["Clients"])
api_v1_router.include_router(
    user_favorite_products_router,
    prefix="/users/{user_uuid}/favorite-products",
    tags=["Favorite products"],
)
api_v1_router.include_router(auth_router, prefix="/auth", tags=["Authentication"])
