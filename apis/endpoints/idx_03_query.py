#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 15:07
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   idx_03_query.py
# @Desc     :   

from fastapi import APIRouter, Query
from typing import Annotated

router = APIRouter()


@router.get("/news")
async def get_news(
        page: Annotated[int, Query(..., description="The page number", ge=1, le=100)] = 1,
        page_size: Annotated[int, Query(..., description="The page size", ge=1, le=10)] = 10
):
    return {"page": page, "page_size": page_size}
