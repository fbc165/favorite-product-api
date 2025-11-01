from typing import Annotated, Self

from pydantic import (
    AfterValidator,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    model_validator,
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
    password: str = Field(min_length=8)


class UpdateUserPayload(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: NameStr | None = None
    email: EmailStr | None = None

    @model_validator(mode="after")
    def validate_if_at_least_one_field_exists(self) -> Self:
        if not self.name and not self.email:
            raise ValueError("At least one field should be updated")
        return self
