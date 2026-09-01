#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 16:47
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   idx_07_depends.py
# @Desc     :   

from fastapi import APIRouter, Query, Depends
from pydantic import validate_call
from typing import Annotated

router = APIRouter()


@validate_call
async def parameters(
        page: Annotated[int, Query(..., ge=1, le=100)] = 1,
        page_size: Annotated[int, Query(..., ge=1, le=10)] = 10
):
    return {"page": page, "page_size": page_size}


@router.get("/movie")
async def get_movie(params: Annotated[dict, Depends(parameters)]):
    return params
