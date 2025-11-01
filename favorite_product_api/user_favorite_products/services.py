import asyncio

import httpx
from sqlalchemy import UUID, select
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_product_api.user_favorite_products.models import UserFavoriteProduct
from favorite_product_api.users.services import UserService


class UserFavoriteProductService:
    async def get_user_favorite_products(
        user_uuid: UUID, db_session: AsyncSession
    ) -> UserFavoriteProduct:

        user = await UserService.get_user(db_session=db_session, uuid=user_uuid)

        favorite_products = await db_session.execute(
            select(UserFavoriteProduct).where(UserFavoriteProduct.user_id == user.id)
        )

        favorite_products = favorite_products.scalars().all()

        async with httpx.AsyncClient() as client:
            tasks = [
                client.get(
                    f"https://fakestoreapi.com/products/{favorite_product.product_id}"
                )
                for favorite_product in favorite_products
            ]
            products = await asyncio.gather(*tasks)

            return [product.json() for product in products]

    async def add_favorite_product_to_user(
        user_uuid: UUID, product_id: int, db_session: AsyncSession
    ) -> dict:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"https://fakestoreapi.com/products/{product_id}",
            )

        response.raise_for_status()

        data = response.json()
        product_id = data["id"]

        user = await UserService.get_user(db_session=db_session, uuid=user_uuid)

        user_favorite_product = UserFavoriteProduct(
            user_id=user.id, product_id=product_id
        )

        db_session.add(user_favorite_product)

        try:
            await db_session.flush()
        except IntegrityError:
            raise ProductAlreadyIsFavoriteError()

        return data
