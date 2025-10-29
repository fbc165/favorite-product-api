from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_product_api.exceptions import NotFoundError
from favorite_product_api.users.models import User


class UserService:
    @classmethod
    async def create_user(cls, db_session: AsyncSession, name: str, email: str) -> User:
        user = User(email=email, name=name)
        db_session.add(user)
        await db_session.flush()

        return user

    @classmethod
    async def update_user(
        cls,
        db_session: AsyncSession,
        uuid: UUID,
        name: str | None = None,
        email: str | None = None,
    ) -> dict:
        updated_data = {}

        query = select(User).where(User.uuid == uuid)
        user = await db_session.execute(query)
        user = user.scalar_one_or_none()

        if user is None:
            raise NotFoundError("User not found")

        if name is not None:
            user.name = name
            updated_data["name"] = user.name

        if email is not None:
            user.email = email
            updated_data["email"] = user.email

        db_session.add(user)

        await db_session.flush()

        return updated_data

    @classmethod
    async def get_user(cls, db_session: AsyncSession, uuid: UUID) -> User:
        query = select(User).where(User.uuid == uuid)
        user = await db_session.execute(query)
        user = user.scalar_one_or_none()

        if user is None:
            raise NotFoundError("User not found")

        return user

    @classmethod
    async def delete_user(cls, db_session: AsyncSession, uuid: UUID) -> bool:
        user = await cls.get_user(db_session=db_session, uuid=uuid)

        db_session.delete(user)

        await db_session.flush()

        return True
