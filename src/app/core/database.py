# from contextlib import asynccontextmanager
from datetime import datetime
from typing import Annotated, AsyncGenerator, Optional, Type, TypeVar

from fastapi import HTTPException
from sqlalchemy import (
    BigInteger,
    String,
    func,
)
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from sqlalchemy.ext.asyncio import (
    AsyncAttrs,
    AsyncSession,
    async_sessionmaker,
    create_async_engine,
)
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    declared_attr,
    mapped_column,
    registry,
)

from app.core.config import settings

engine = create_async_engine(settings.get_db_url())
async_session_maker = async_sessionmaker(
    engine, expire_on_commit=False, autoflush=False)

created_at = Annotated[datetime, mapped_column(
    server_default=func.now(timezone=True))]
updated_at = Annotated[datetime, mapped_column(
    server_default=func.now(timezone=True), onupdate=func.now(timezone=True))]
# str_email = Annotated[str, settings.MAX_LENGTH_EMAIL]
# str_username = Annotated[str, mapped_column(
#     String(settings.MAX_LENGTH_USERNAME), unique=True, nullable=False)]
# str_name_template = Annotated[str, mapped_column(
#     String(settings.MAX_LENGTH_NAME_TEMPLATE), unique=True, nullable=False)]
# str_nullable = Annotated[str, mapped_column(nullable=True)]


class Base(AsyncAttrs, DeclarativeBase):
    """Базовый класс модели с описанием стандартных полей."""

    __abstract__ = True
    # registry = registry(
    #     type_annotation_map={
    #         str_email: String(settings.MAX_LENGTH_EMAIL)})

    @declared_attr.directive
    def __tablename__(cls) -> str:  # noqa: N805
        return cls.__name__.lower() + 's'

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True)
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


ModelType = TypeVar('ModelType', bound=Base)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """Создание сессий для подключения к БД."""
    async with async_session_maker() as async_session:
        try:
            yield async_session
        except SQLAlchemyError as e:
            await async_session.rollback()
            raise HTTPException(
                status_code=500,
                detail=f'Ошибка работы с БД: {str(e)}')
        finally:
            await async_session.close()


# @asynccontextmanager
# async def get_session_for_lifespan() -> AsyncGenerator[AsyncSession, None]:
#     """Создание сессий для подключения к БД lifespan задач."""
#     async for session in get_async_session():
#         yield session


async def commit_change(
    session: AsyncSession,
    obj: Optional[Type[ModelType]] = None,
) -> Optional[ModelType]:
    """Безопасное выполнение действий с БД."""
    try:
        await session.commit()
        if obj:
            await session.refresh(obj)
    except IntegrityError as e:
        await session.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"Ошибка целостности данных: {str(e.orig)}")
    except SQLAlchemyError as e:
        await session.rollback()
        raise HTTPException(
            status_code=500,
            detail=f'Ошибка сохранения в БД: {str(e)}')
    else:
        return obj
