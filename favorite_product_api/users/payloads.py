from pydantic import BaseModel, EmailStr, field_validator


class CreateUserPayload(BaseModel):
    name: str
    email: EmailStr

    @field_validator("name")
    @classmethod
    def validate_name(cls, value: str) -> str:
        if not value:
            ValueError("name cannot be empty")

        prepositions = ["e", "de", "da", "do", "dos", "das"]

        return " ".join(
            word.capitalize() if word.lower() not in [prepositions] else word.lower()
            for word in value.strip().split()
        )
