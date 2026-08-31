#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/8/31 23:19
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   main.py
# @Desc     :   

from fastapi import FastAPI, Path
from uvicorn import run

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/hello/{username}")
async def say_hello(
        name: str = Path(
            alias="username",
            # If you want to use a different name for the parameter, align with parameter in router and function
            description="The name of the user to greet",
            min_length=2,
            max_length=10,
        )
):
    return {"message": f"Hello {name}"}


if __name__ == "__main__":
    run(app, host="0.0.0.0", port=8000)
