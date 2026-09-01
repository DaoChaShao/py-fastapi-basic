#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 15:05
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   idx_01_hello.py
# @Desc     :   

from fastapi import APIRouter, Path

router = APIRouter()


@router.get("/hello/{name}")
async def say_hello(
        name: str = Path(
            ...,
            description="The name of the user to greet",
            min_length=2,
            max_length=10,
        )
):
    return {"message": f"Hello {name}"}
