from sqlalchemy import select

from app.database import async_session_maker
from app.models import User


async def create_user(user_data: dict):
    async with async_session_maker() as session:
        async with session.begin():
            new_user = User(**user_data)
            session.add(new_user)
            await session.commit()
            return new_user


async def get_auth_user_or_none(email: str):
    async with async_session_maker() as session:
        query = select(User).where(User.email == email)
        result = await session.execute(query)
        user = result.scalar_one_or_none()
        return user
