from fastapi import APIRouter

from favorite_product_api.users.routes import router as users_router

api_v1_router = APIRouter()

api_v1_router.include_router(users_router, prefix="/users", tags=["Users"])
