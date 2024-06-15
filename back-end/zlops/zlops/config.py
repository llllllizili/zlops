#!/usr/bin python
# -*- encoding: utf-8 -*-
"""
@File    :    config.py
@Time    :   2024/06/03 08:42:25
"""
import os

# 基本配置
DEBUG = os.getenv("DEBUG", True)

SECRET_KEY = "sk2lw67kei6cdmno"
BASE_PROJECT_CODE = "zlops"  # 一旦配置不要变
CREATE_USER_DEFAULT_PASSWORD = os.getenv(
    "CREATE_USER_DEFAULT_PASSWORD", "123456"
)  # 为设置密码时候，默认密码

# 数据库
MYSQL_DB_NAME = os.getenv("MYSQL_DB_NAME", "zlops")
MYSQL_DB_HOST = os.getenv("MYSQL_DB_HOST", "127.0.0.1")
MYSQL_DB_PORT = os.getenv("MYSQL_DB_PORT", 3306)
MYSQL_DB_USER = os.getenv("MYSQL_DB_USER", "root")
MYSQL_DB_PASSWORD = os.getenv("MYSQL_DB_PASSWORD", "Password_1")

# Redis 配置
REDIS_USER = os.getenv("REDIS_USER", "default")
REDIS_PASSWORD = os.getenv("REDIS_PASSWORD", "123qweASD")
REDIS_ADDRESS = os.getenv("REDIS_ADDRESS", "127.0.0.1")
REDIS_PORT = os.getenv("REDIS_PORT", "6379")
REDIS_CACHES_DB = os.getenv("REDIS_CACHES_DB", 1)
REDIS_CELERY_BROKER_DB = os.getenv("REDIS_CELERY_BROKER_DB", 2)
REDIS_CHANNEL_DB = os.getenv("REDIS_CHANNEL_DB", 3)

# 邮箱配置
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.qq.com")
EMAIL_PORT = os.getenv("EMAIL_PORT", 587)  # 465
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_PASSWORD", None)
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD", None)
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", True)