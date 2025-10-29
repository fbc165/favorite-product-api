from uuid import UUID

from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    uuid: UUID
    email: str
    name: str
