#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 15:33
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   idx_05_response_02_html.py
# @Desc     :   

from fastapi import APIRouter
from fastapi.responses import HTMLResponse

router = APIRouter()


@router.get("/html", response_class=HTMLResponse)
async def get_html():
    return f"<h1>Hello, World!</h1>"
