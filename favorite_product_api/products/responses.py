from typing import Union

from pydantic import BaseModel, HttpUrl


class ProductResponse(BaseModel):
    id: int
    title: str
    image: HttpUrl
    price: float
    description: str
    category: str
    rating: dict[str, Union[float, int]] | None = None
