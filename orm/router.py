#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 17:03
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   router.py
# @Desc     :   

from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, Query, Path
from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.sql import func
from typing import Annotated, Any, Self, Union, Literal

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
        name: Annotated[str, Query(min_length=1, max_length=100, description="Book name")],
        price: Annotated[int, Query(gt=0, le=9999, description="Book price")],
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


@router.put("/books")
async def update_book(
        idx: Annotated[int, Query(ge=1, description="Book index")],
        name: Annotated[str, Query(min_length=1, max_length=100, description="Book name")],
        price: Annotated[int, Query(gt=0, le=9999, description="Book price")],
        session: AsyncSession = Depends(get_session)
) -> BookCreation:
    """ Update a book by index. """
    book = await session.get(Books, idx)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book not found yet! Please create it first. IDX: {idx}.")
    book.name = name
    book.price = price
    await session.commit()
    await session.refresh(book)
    return BookCreation.from_orm(book)


@router.delete("/books")
async def delete_book(
        idx: Annotated[int, Query(ge=1, description="Book index")],
        session: AsyncSession = Depends(get_session)
) -> BookCreation:
    """ Delete a book by index. """
    book = await session.get(Books, idx)
    if book is None:
        raise HTTPException(status_code=404, detail=f"Book not found yet! Please create it first. IDX: {idx}.")
    await session.delete(book)
    await session.commit()
    return BookCreation.from_orm(book)


@router.get("/books/pages")
async def get_content_by_layout(
        page: Annotated[int, Query(ge=1, description="Page number")] = 1,
        page_size: Annotated[int, Query(ge=1, le=100, description="Items per page")] = 1,
        session: AsyncSession = Depends(get_session)
) -> BookResponse:
    """ Get a list of books by page and page size. """
    offset = (page - 1) * page_size
    result = await session.execute(select(Books).offset(offset).limit(page_size).order_by(Books.idx))
    books = result.scalars().all()
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


@router.get("/bools/like/{name}")
async def query_by_name(
        name: Annotated[str, Path(min_length=1, max_length=10, description="Book name")],
        session: AsyncSession = Depends(get_session)
) -> BookResponse:
    """ Get a book by name. """
    result = await session.execute(select(Books).where(Books.name.like(f"%{name}%")))
    books = result.scalars().all()
    if not books:
        raise HTTPException(status_code=404, detail=f"No books found with name: {name}")
    return BookResponse(messages="Books found", books=[BookCreation.from_orm(book) for book in books])


@router.get("books/agg/{category}")
async def agg_data(
        category: Annotated[
            Union[str, Literal["avg", "count", "max", "min", "sum"]],
            Path(min_length=1, max_length=10, description="Aggregation type")
        ],
        session: AsyncSession = Depends(get_session)
) -> dict[str, Any]:
    """ Get a book by name. """
    match category:
        case "avg":
            result = await session.execute(select(func.avg(Books.price)))
        case "count":
            result = await session.execute(select(func.count(Books.idx)))
        case "max":
            result = await session.execute(select(func.max(Books.price)))
        case "min":
            result = await session.execute(select(func.min(Books.price)))
        case "sum":
            result = await session.execute(select(func.sum(Books.price)))
        case _:
            raise HTTPException(status_code=404, detail=f"No books found with name: {category}")
    num = result.scalars()
    return {"messages": "Aggregation Done!", "number": num}
