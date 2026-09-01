#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 17:03
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   router.py
# @Desc     :   

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import Field, BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated, Any, Self

from .endpoints.datasets import get_session, Books

router = APIRouter()


class BookCreation(BaseModel):
    idx: int
    name: str
    price: float
    create_time: datetime
    update_time: datetime

    @classmethod
    def from_orm(cls, obj: Any) -> Self:
        """ Create a BookResponse object from an ORM object. """
        return cls(
            idx=obj.idx,
            name=obj.name,
            price=obj.price,
            create_time=obj.create_time,
            update_time=obj.update_time
        )


class BookResponse(BaseModel):
    messages: str
    books: list[BookCreation]


@router.post("/books", response_model=BookCreation)
async def create_book(
        name: Annotated[str, Field(min_length=1, max_length=100, description="Book name")],
        price: Annotated[int, Field(gt=0, le=9999, description="Book price")],
        session: AsyncSession = Depends(get_session)
) -> BookCreation:
    book = Books(name=name, price=price)
    session.add(book)
    await session.commit()
    await session.refresh(book)
    return BookCreation.from_orm(book)


@router.get("/books", response_model=BookResponse)
async def get_books(session: AsyncSession = Depends(get_session)) -> BookResponse:
    """ Get a list of all books. """
    books = await session.execute(select(Books))
    books = books.scalars().all()
    return BookResponse(messages="Books found", books=[BookCreation.from_orm(book) for book in books])


@router.get("/books/query")
async def get_low_price_items(
        price: Annotated[int, Query(gt=0, le=9999, description="Get books with price less than or equal to")],
        session: AsyncSession = Depends(get_session)
) -> BookResponse:
    """ Get a book by price. """
    result = await session.execute(select(Books).where(Books.price <= price))
    books = result.scalars().all()
    if not books:
        raise HTTPException(status_code=404, detail=f"No books found with price <= {price}")
    return BookResponse(messages="Books found", books=[BookCreation.from_orm(book) for book in books])


@router.get("/books/search/{price}")
async def get_high_price_item(
        price: Annotated[int, Path(gt=0, le=9999, description="Get books with price greater than or equal to")],
        session: AsyncSession = Depends(get_session)
) -> BookResponse:
    """ Get a book by price. """
    result = await session.execute(select(Books).where(Books.price >= price))
    books = result.scalars().all()
    if not books:
        raise HTTPException(status_code=404, detail=f"No books found with price >= {price}")
    return BookResponse(messages="Books found", books=[BookCreation.from_orm(book) for book in books])


@router.get("/books/{idx}")
async def get_book(idx: int, session: AsyncSession = Depends(get_session)) -> BookCreation:
    """ Get a book by index. """
    # Method I
    # book = await session.execute(select(Books).where(Books.idx == idx))
    # book = book.scalars().first()
    # Method II
    book = await session.get(Books, idx)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book not found yet! Please create it first. IDX: {idx}.")
    return BookCreation.from_orm(book)
