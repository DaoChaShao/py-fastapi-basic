#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 16:05
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   idx_06_exception.py
# @Desc     :   

from fastapi import APIRouter, HTTPException

router = APIRouter()


@router.get("/book/{idx}")
async def get_book(idx: int):
    if idx == 1:
        return {"index": idx, "title": "1984", "author": "George Orwell"}
    else:
        raise HTTPException(status_code=404, detail="Book not found")
