from typing import Annotated

from pydantic import BaseModel, Field


class AddFavoriteProductPayload(BaseModel):
    id: Annotated[int, Field(ge=0)]
