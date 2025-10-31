from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_product_api.databases.postgresql import get_db
from favorite_product_api.exceptions import NotFoundError
from favorite_product_api.user_favorite_products.payloads import (
    AddFavoriteProductPayload,
)
from favorite_product_api.user_favorite_products.responses import (
    AddUserFavoriteProductResponse,
    GetUserFavoriteProductsResponse,
    ProductItem,
)
from favorite_product_api.user_favorite_products.services import (
    UserFavoriteProductService,
)

router = APIRouter()


@router.post("/")
async def add_favorite_product(
    user_uuid: UUID,
    payload: AddFavoriteProductPayload,
    db_session: AsyncSession = Depends(get_db),
):
    try:
        user_favorite_product = (
            await UserFavoriteProductService.add_favorite_product_to_user(
                db_session=db_session, user_uuid=user_uuid, product_id=payload.id
            )
        )

        return AddUserFavoriteProductResponse(
            product_id=user_favorite_product["id"],
            title=user_favorite_product["title"],
            image=user_favorite_product["image"],
            price=user_favorite_product["price"],
        )

    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )


@router.get("/")
async def get_user_favorite_products(
    user_uuid: UUID, db_session: AsyncSession = Depends(get_db)
):
    try:
        favorite_products = await UserFavoriteProductService.get_user_favorite_products(
            db_session=db_session, user_uuid=user_uuid
        )

        return GetUserFavoriteProductsResponse(
            products=[
                ProductItem(
                    product_id=favorite_product["id"],
                    title=favorite_product["title"],
                    image=favorite_product["image"],
                    price=favorite_product["price"],
                )
                for favorite_product in favorite_products
            ]
        )
    except NotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))

    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Internal server error",
        )
