#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 15:28
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   idx_05_response_01_json.py
# @Desc     :   

from fastapi import APIRouter
from fastapi.responses import JSONResponse
from pydantic import BaseModel, Field
from typing import Annotated

router = APIRouter()


class User(BaseModel):
    username: Annotated[str, Field(default="Admin", description="The username", min_length=2, max_length=10)]
    password: Annotated[str, Field(default="12345", description="The password", min_length=5, max_length=20)]


@router.post("/login", response_class=JSONResponse)
async def login(user: User):
    return {"username": user.username, "password": user.password}
