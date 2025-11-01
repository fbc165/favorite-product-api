from typing import Annotated

from pydantic import BaseModel, EmailStr, Field


class UserLoginPayload(BaseModel):
    email: EmailStr
    password: Annotated[str, Field(min_length=8, max_length=60)]
