#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 16:30
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   right.py
# @Desc     :   

from fastapi import FastAPI, Request


def right_middleware(app: FastAPI):
    @app.middleware("http")
    async def middleware_right(request: Request, call_next):
        print("Middleware Right Start")
        response = await call_next(request)
        print("Middleware Right End")
        return response
