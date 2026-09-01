#!/usr/bin/env python3.12
# -*- Coding: UTF-8 -*-
# @Time     :   2026/9/1 15:09
# @Author   :   Shawn
# @Version  :   Version 0.1.0
# @File     :   router.py
# @Desc     :   

from fastapi import APIRouter
from .endpoints import (idx_01_hello,
                        idx_02_hi,
                        idx_03_query,
                        idx_04_body,
                        idx_05_response_01_json,
                        idx_05_response_02_html,
                        idx_05_response_03_file,
                        idx_05_response_04_customise,
                        idx_06_exception,
                        idx_07_depends)

router = APIRouter()

# Register the routers
router.include_router(idx_01_hello.router, tags=["Hello"])
router.include_router(idx_02_hi.router, tags=["Hi"])
router.include_router(idx_03_query.router, tags=["News"])
router.include_router(idx_04_body.router, tags=["Body"])
router.include_router(idx_05_response_01_json.router, tags=["Json Response"])
router.include_router(idx_05_response_03_file.router, tags=["File Response"])
router.include_router(idx_05_response_02_html.router, tags=["HTML Response"])
router.include_router(idx_05_response_04_customise.router, tags=["Customise Response"])
router.include_router(idx_06_exception.router, tags=["Exception"])
router.include_router(idx_07_depends.router, tags=["Depends"])
