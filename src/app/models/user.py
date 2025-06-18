from fastapi import Depends
from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseUserTable,
    SQLAlchemyUserDatabase
)
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import Base, get_async_session


class User(Base, SQLAlchemyBaseUserTable[int]):
    # add ext fields
    pass

    @classmethod
    async def get_user_db(
        cls,
        session: AsyncSession = Depends(get_async_session)
    ):
        yield SQLAlchemyUserDatabase(session, User)
