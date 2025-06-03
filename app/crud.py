import random
import string
from typing import List
from datetime import datetime, timezone
from fastapi import HTTPException
from sqlalchemy import select
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.sql.expression import update
from pydantic import HttpUrl

from app.database import async_session_maker
from app.models import URL
from app.schemas import URLSchema


async def original_url_by_alias(alias: str) -> URLSchema | None:
    async with async_session_maker() as session:
        try:
            query = select(URL).where(URL.alias == alias)
            result = await session.execute(query)
            original_url = result.scalar_one_or_none()

            if original_url is None:
                raise HTTPException(status_code=404, detail="Alias not found")

            if (
                original_url.expires_at <= datetime.now(timezone.utc)
                or not original_url.is_active
            ):
                raise HTTPException(status_code=410, detail="Alias is deactivated")

            return original_url

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error")


async def click_count(alias: str) -> None:
    async with async_session_maker() as session:
        try:
            async with session.begin():
                await session.execute(
                    update(URL).where(URL.alias == alias).values(count=URL.count + 1)
                )

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error")


async def create_alias(httpurl: HttpUrl) -> URLSchema | None:
    url = str(httpurl)

    async with async_session_maker() as session:
        alias = "".join(
            random.choice(string.ascii_letters + string.digits) for _ in range(8)
        )
        create_url = URL(original_url=url, alias=alias)
        try:
            session.add(create_url)
            await session.commit()
            return URLSchema.model_validate(create_url)

        except SQLAlchemyError as e:
            print(e)
            await session.rollback()
            raise HTTPException(status_code=500, detail="Failed to create alias")


async def all_aliases(skip: int, limit: int) -> List[str]:
    async with async_session_maker() as session:
        try:
            query = (
                select(URL.alias)
                .where(
                    (URL.expires_at > datetime.now(timezone.utc))
                    & (URL.is_active == True)
                )
                .offset(skip)
                .limit(limit)
            )
            result = await session.execute(query)
            alias = result.scalars().all()
            return alias

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error")


async def deactivation_alias(alias: str):
    async with async_session_maker() as session:
        try:
            async with session.begin():
                stmt = select(URL.is_active).where(URL.alias == alias)
                result = await session.execute(stmt)
                current_status = result.scalar_one_or_none()

                if current_status is None:
                    raise HTTPException(status_code=404, detail="Alias not found")

                if not current_status:
                    return {"status": "already_deactivated", "deactivated": 0}

                update_query = (
                    update(URL).where(URL.alias == alias).values(is_active=False)
                )
                await session.execute(update_query)

                return {"status": "success", "deactivated": 1}

        except SQLAlchemyError as e:
            raise HTTPException(status_code=500, detail="Database error")
