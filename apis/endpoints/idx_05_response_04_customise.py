#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 15:59
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   idx_05_response_04_customise.py
# @Desc     :   

from fastapi import APIRouter
from pydantic import BaseModel, Field
from typing import Annotated

router = APIRouter()


class Item(BaseModel):
    name: Annotated[str, Field(min_length=1)]
    description: Annotated[str, Field(min_length=1, max_length=100)]
    price: Annotated[float, Field(gt=0)]
    tax: Annotated[float, Field(gt=0, description="The price must be greater than zero")]


@router.get("/customise", response_model=Item)
async def get_item():
    return Item(name="Foo", description="A very nice Item", price=35.4, tax=3.2)
