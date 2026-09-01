#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 16:29
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   left.py
# @Desc     :   

from fastapi import FastAPI, Request


def left_middleware(app: FastAPI):
    @app.middleware("http")
    async def middleware_left(request: Request, call_next):
        print("Middleware Left Start")
        response = await call_next(request)
        print("Middleware Left End")
        return response
