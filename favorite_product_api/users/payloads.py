from typing import Annotated

from pydantic import (
    AfterValidator,
    BaseModel,
    EmailStr,
    Field,
)


def validate_name(name: str) -> str:
    if not name:
        raise ValueError("Name cannot be empty")

    prepositions = ["e", "de", "da", "do", "dos", "das"]

    return " ".join(
        word.capitalize() if word.lower() not in [prepositions] else word.lower()
        for word in name.strip().split()
    )


NameStr = Annotated[
    str, Field(max_length=100, min_length=1), AfterValidator(validate_name)
]


class CreateUserPayload(BaseModel):
    name: NameStr
    email: EmailStr
