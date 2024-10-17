# -*- coding:utf-8 -*-
"""

"""

import os
from dotenv import load_dotenv, find_dotenv
from typing import List

from pydantic.v1 import BaseSettings


class Config(BaseSettings):
    # 加载环境变量
    load_dotenv(find_dotenv(), override=True)
    # 调试模式
    APP_DEBUG: bool = True
    # 项目信息
    VERSION: str = "0.0.1"
    PROJECT_NAME: str = "任务管理系统"
    # 静态资源目录
    # STATIC_DIR: str = os.path.join(os.getcwd(), "static")
    # TEMPLATE_DIR: str = os.path.join(STATIC_DIR, "templates")
    # 跨域请求
    PROJECT_TITLE: str = "任务管理系统"
    CORS_ORIGINS: List = ["*"]   # 允许的来源
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List = ["*"]
    CORS_ALLOW_HEADERS: List = ["*"]
    # Session
    # SECRET_KEY = "session"
    # SESSION_COOKIE = "session_id"
    # SESSION_MAX_AGE = 14 * 24 * 60 * 60
    # Jwt
    # JWT_SECRET_KEY = "09d25e094faa6ca2556c818166b7a9563b93f7099f6f0f4caa6cf63b88e8d3e7"
    # JWT_ALGORITHM = "HS256"
    # JWT_ACCESS_TOKEN_EXPIRE_MINUTES = 24 * 60
    orm_config = {
        'connections': {
            'default': {
                'engine': 'tortoise.backends.mysql',
                'credentials': {
                    'host': '1.94.234.64',
                    'port': '3306',
                    'user': 'task',
                    'password': '123456',
                    'database': 'task',
                    'charset': 'utf8mb4',
                    'echo': True
                }
            },
        },
        'apps': {
            'models': {
                'models': ['task.models', 'aerich.models'],
                'default_connection': 'default',
            }
        }
    }


settings = Config()
