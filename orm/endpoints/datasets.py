#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 17:06
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   datasets.py
# @Desc     :   

from datetime import datetime
from pydantic import validate_call, Field
from pathlib import Path
from sqlalchemy import create_engine, Engine
from sqlalchemy.ext.asyncio import create_async_engine, AsyncEngine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy.sql import func
from sqlalchemy.types import DateTime, Integer, String, Float
from typing import Union, Annotated, TypeGuard


@validate_call
def init_sqlite_engine(
        db_path: Union[str, Path],
        *,
        is_async: Annotated[bool, Field(description="Whether to use asynchronous database connection")] = False,
        echo: Annotated[bool, Field(description="Whether to echo the SQL statements")] = True,
        future: Annotated[bool, Field(description="Whether to use the future API")] = True,
        pool_size: Annotated[int, Field(ge=0, description="Connection pool size")] = 10,
        max_overflow: Annotated[int, Field(gt=-1, description="Max overflow connections")] = 20
) -> Union[Engine, AsyncEngine]:
    """
    Initialise the database connection.

    :param db_path: The path to the database file.
    :param is_async: If True, use aiosqlite for async support (default: True).
    :param echo: If True, logs all SQL statements (default: True).
    :param future: If True, uses the 2.0 style API (default: True).
    :param pool_size: Connection pool size (default: 10, must be >= 0).
    :param max_overflow: Max overflow connections (default: 20, must be > -1).
    :return: SQLAlchemy Engine instance.
    """
    # Resolve path
    _path = Path(db_path).resolve()

    match is_async:
        case True:
            return create_async_engine(
                f"sqlite+aiosqlite:///{_path}",
                echo=echo,
                future=future,
                pool_size=pool_size,
                max_overflow=max_overflow
            )
        case False:
            return create_engine(f"sqlite:///{_path}", echo=echo)
        case _:
            raise ValueError("Invalid value for async")


def is_async_engine(engine: Union[Engine, AsyncEngine]) -> TypeGuard[AsyncEngine]:
    """
    Check if the engine is an async engine.

    :param engine: The engine to check.
    :return: True if the engine is async, False otherwise.
    """
    return hasattr(engine, "connect") and hasattr(engine.connect(), "__aenter__")


class ORMTypes:
    PK: Mapped[int] = Annotated[
        int,
        mapped_column(Integer, primary_key=True, autoincrement=True, nullable=False, comment="Primary Key")
    ]
    CT: Mapped[datetime] = Annotated[
        datetime,
        mapped_column(DateTime, server_default=func.now(), nullable=False, comment="Create Time")
    ]
    UT: Mapped[datetime] = Annotated[
        datetime,
        mapped_column(DateTime, server_default=func.now(), onupdate=func.now(), nullable=False, comment="Update Time")
    ]
    NAME: Mapped[str] = Annotated[
        str,
        mapped_column(String(100), nullable=False, comment="Name")
    ]


Base = declarative_base()


class Abs(Base):
    __abstract__ = True

    create_time: Mapped[ORMTypes.CT]
    update_time: Mapped[ORMTypes.UT]


class Books(Abs):
    __tablename__ = "books"
    __table_args__ = {"comment": "Books Table"}

    idx: Mapped[ORMTypes.PK]
    name: Mapped[ORMTypes.NAME]
    price: Mapped[float] = mapped_column(Float(), nullable=False, comment="Price")


ENGINE: AsyncEngine = init_sqlite_engine("./data/db.sqlite3", is_async=True, echo=True)


async def init_db():
    """ Initialise the database. """
    async with ENGINE.connect() as connection:
        await connection.run_sync(Base.metadata.create_all)
        await connection.commit()


async def close_db():
    """ Close the database connection. """
    await ENGINE.dispose()


SESSION: async_sessionmaker = async_sessionmaker(
    bind=ENGINE,
    class_=AsyncSession,
    expire_on_commit=False
)


async def get_session():
    """ Get a database session. """
    async with SESSION() as session:
        yield session
