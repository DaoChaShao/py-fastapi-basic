#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 15:07
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   idx_02_hi.py
# @Desc     :   

from fastapi import APIRouter, Path
from typing import Annotated

router = APIRouter()


@router.get("/hi/{username}")
async def say_hi(
        name: Annotated[
            str,
            Path(
                ...,
                alias="username",
                # If you want to use a different name for the parameter, align with parameter in router and function
                description="The name of the user to greet",
                min_length=2,
                max_length=10,
                examples=["Tome", "Jerry"]
            )
        ]
):
    return {"message": f"Hi {name}"}
