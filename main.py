#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/8/31 23:19
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   main.py
# @Desc     :   

from contextlib import asynccontextmanager
from fastapi import FastAPI
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from uvicorn import run

from apis.router import router as api_router
from orm.router import router as orm_router
from middlewares import left_middleware, right_middleware

from orm.endpoints.datasets import (init_db, close_db,
                                    SESSION, Books)


@asynccontextmanager
async def lifespan(_: FastAPI):
    await init_db()
    print("Database initialized")

    async with SESSION() as session:
        result = await session.execute(select(Books))
        books = result.scalars().all()
        print(f"Found {len(books)} books")
        for book in books:
            print(f" - {book.name} (${book.price})")

    yield
    await close_db()
    print("Database closed")


app = FastAPI(
    title="FastAPI Application",
    description="A modular FastAPI application",
    version="0.1.0",
    lifespan=lifespan,
)

# left_middleware(app)
# right_middleware(app)

# app.include_router(api_router, prefix="/apis")
app.include_router(orm_router, prefix="/orm")


@app.get("/")
async def root():
    return {"message": "Hello World"}


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000, reload=True, log_level="info")
