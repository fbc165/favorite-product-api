from typing import Union

from pydantic import BaseModel, HttpUrl


class ProductItem(BaseModel):
    product_id: int
    title: str
    image: HttpUrl
    price: float
    rating: dict[str, Union[int, float]] | None = None


class GetUserFavoriteProductsResponse(BaseModel):
    products: list[ProductItem]


class AddUserFavoriteProductResponse(BaseModel):
    product_id: int
    title: str
    image: HttpUrl
    price: float
    rating: dict[str, Union[int, float]] | None = None
