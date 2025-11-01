from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from favorite_product_api.auth.security import get_password_hash
from favorite_product_api.exceptions import EmailAlreadyExistsError, NotFoundError
from favorite_product_api.users.models import User


class UserService:
    @classmethod
    async def create_user(
        cls, db_session: AsyncSession, name: str, email: str, password: str
    ) -> User:
        hashed_password = get_password_hash(password)
        user = User(email=email, name=name, hashed_password=hashed_password)
        db_session.add(user)
        await db_session.flush()

        return user

    @classmethod
    async def get_user(cls, db_session: AsyncSession, uuid: UUID) -> User:
        query = select(User).where(User.uuid == uuid)
        user = await db_session.execute(query)
        user = user.scalar_one_or_none()

        if user is None:
            raise NotFoundError("User not found")

        return user

    @classmethod
    async def get_user_by_email(cls, db_session: AsyncSession, email: str) -> User:
        query = select(User).where(User.email == email)
        user = await db_session.execute(query)
        user = user.scalar_one_or_none()

        if user is None:
            raise NotFoundError("User not found")

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

        user = await cls.get_user(db_session=db_session, uuid=uuid)

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
    async def delete_user(cls, db_session: AsyncSession, uuid: UUID) -> None:
        user = await cls.get_user(db_session=db_session, uuid=uuid)

        await db_session.delete(user)

        await db_session.flush()

        return
