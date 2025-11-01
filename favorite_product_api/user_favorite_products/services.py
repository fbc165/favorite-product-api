from sqlalchemy import UUID, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_product_api.exceptions import NotFoundError, ProductAlreadyIsFavoriteError
from favorite_product_api.products.datasources import ProductDataSource
from favorite_product_api.products.responses import ProductResponse
from favorite_product_api.user_favorite_products.models import UserFavoriteProduct
from favorite_product_api.users.services import UserService


class UserFavoriteProductService:
    async def get_user_favorite_products(
        user_uuid: UUID, db_session: AsyncSession
    ) -> list[ProductResponse]:

        user = await UserService.get_user(db_session=db_session, uuid=user_uuid)

        favorite_products = await db_session.execute(
            select(UserFavoriteProduct).where(UserFavoriteProduct.user_id == user.id)
        )

        favorite_products = favorite_products.scalars().all()

        products = await ProductDataSource.get_products_by_ids(
            ids=[favorite_product.product_id for favorite_product in favorite_products]
        )

        return [
            ProductResponse(
                id=product.json()["id"],
                title=product.json()["title"],
                image=product.json()["image"],
                price=product.json()["price"],
                description=product.json()["description"],
                category=product.json()["category"],
                rating=product.json()["rating"],
            )
            for product in products
        ]

    async def add_favorite_product_to_user(
        user_uuid: UUID, product_id: int, db_session: AsyncSession
    ) -> ProductResponse:
        response = await ProductDataSource.get_product_by_id(id=product_id)

        response.raise_for_status()

        if not response.content:
            raise NotFoundError("Product not found")

        product_data = response.json()

        try:
            product = ProductResponse(
                id=product_data["id"],
                title=product_data["title"],
                image=product_data["image"],
                price=product_data["price"],
                description=product_data["description"],
                category=product_data["category"],
                rating=product_data["rating"],
            )
        except KeyError:
            raise NotFoundError("Product not found")

        user = await UserService.get_user(db_session=db_session, uuid=user_uuid)

        user_favorite_product = UserFavoriteProduct(
            user_id=user.id, product_id=product.id
        )

        db_session.add(user_favorite_product)

        try:
            await db_session.flush()
        except IntegrityError:
            raise ProductAlreadyIsFavoriteError()

        return product

    @classmethod
    async def remove_favorite_product(
        cls, db_session: AsyncSession, user_id: int, product_id: int
    ):
        query = select(UserFavoriteProduct).where(
            UserFavoriteProduct.user_id == user_id,
            UserFavoriteProduct.product_id == product_id,
        )

        result = await db_session.execute(query)
        favorite_product = result.scalar_one_or_none()

        if favorite_product is None:
            raise NotFoundError("Favorite product not found for this user")

        await db_session.delete(favorite_product)

        await db_session.flush()
