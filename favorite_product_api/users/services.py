from sqlalchemy.ext.asyncio import AsyncSession

from favorite_product_api.users.models import User


class UserService:
    @classmethod
    async def create_user(cls, db_session: AsyncSession, name, email) -> User:
        user = User(email=email, name=name)
        db_session.add(user)
        await db_session.flush()

        return user
