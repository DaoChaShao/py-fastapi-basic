#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 15:36
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   idx_05_response_03_file.py
# @Desc     :   

from fastapi import APIRouter
from fastapi.responses import FileResponse

router = APIRouter()


@router.get("/file", response_class=FileResponse)
async def get_file():
    filepath: str = "./data/cat.png"
    return FileResponse(filepath, filename="cat.png")
