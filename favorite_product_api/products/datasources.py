import asyncio

from httpx import AsyncClient, Response

from favorite_product_api.settings import settings


class ProductDataSource:
    @classmethod
    async def get_products_by_ids(cls, ids: list[int]) -> list[Response]:
        async with AsyncClient() as client:
            tasks = [client.get(f"{settings.PRODUCT_API_URL}/{id}") for id in ids]

            return await asyncio.gather(*tasks)

    @classmethod
    async def get_product_by_id(cls, id: int) -> Response:
        async with AsyncClient() as client:
            return await client.get(f"{settings.PRODUCT_API_URL}/{id}")
