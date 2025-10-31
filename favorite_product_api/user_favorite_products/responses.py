from pydantic import BaseModel, HttpUrl


class ProductItem(BaseModel):
    product_id: int
    title: str
    image: HttpUrl
    price: float


class GetUserFavoriteProductsResponse(BaseModel):
    products: list[ProductItem]


class AddUserFavoriteProductResponse(BaseModel):
    product_id: int
    title: str
    image: HttpUrl
    price: float
