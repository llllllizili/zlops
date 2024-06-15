#!/usr/bin python
# -*- encoding: utf-8 -*-
"""
@File    :    config.py
@Time    :   2024/06/03 08:42:25
"""

# 基本配置
SECRET_KEY = "sk2lw67kei6cdmno"
BASE_PROJECT_CODE = "zlops"  # 一旦配置不要变
CREATE_USER_DEFAULT_PASSWORD = "123456"  # 为设置密码时候，默认密码

# 数据库
MYSQL_DB_NAME="zlops"
MYSQL_DB_HOST="127.0.0.1"
MYSQL_DB_PORT="3306"
MYSQL_DB_USER="root"
MYSQL_DB_PASSWORD="Password_1"


# Redis 配置
REDIS_USER = "default"
REDIS_PASSWORD = "123qweASD"
REDIS_ADDRESS = "127.0.0.1"
REDIS_PORT = "6379"
REDIS_CACHES_DB = 1
REDIS_CELERY_BROKER_DB = 2
REDIS_CHANNEL_DB = 3

# 邮箱配置
EMAIL_HOST = "xx"
EMAIL_PORT = 25
EMAIL_HOST_USER = "xx"
EMAIL_HOST_PASSWORD = "xx"
EMAIL_USE_TLS = True




# setting 
DEBUG = True
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": MYSQL_DB_NAME,
        "USER": MYSQL_DB_USER,
        "PASSWORD": MYSQL_DB_PASSWORD,
        "HOST": MYSQL_DB_HOST,
        "PORT": MYSQL_DB_PORT,
        "OPTIONS": {
            "autocommit": True,
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
# Redis缓存配置
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://{user}:{pwd}@{address}:{port}/{db}".format(
            user=REDIS_USER,
            pwd=REDIS_PASSWORD,
            address=REDIS_ADDRESS,
            port=REDIS_PORT,
            db=REDIS_CACHES_DB,
        ),
    }
}
# ASGI (Channels)
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                "redis://{user}:{pwd}@{address}:{port}/{db}".format(
                    user=REDIS_USER,
                    pwd=REDIS_PASSWORD,
                    address=REDIS_ADDRESS,
                    port=REDIS_PORT,
                    db=REDIS_CHANNEL_DB,
                )
            ],
            "symmetric_encryption_keys": [SECRET_KEY],
            # "capacity": 1500,
            # "expiry": 10,
        },
    },
}


# celery
CELERY_BROKER_URL = "redis://{user}:{pwd}@{address}:{port}/{db}".format(
    user=REDIS_USER,
    pwd=REDIS_PASSWORD,
    address=REDIS_ADDRESS,
    port=REDIS_PORT,
    db=REDIS_CELERY_BROKER_DB,
)
CELERY_TASK_DEFAULT_QUEUE = BASE_PROJECT_CODE
CELERY_WORKER_CONCURRENCY = 4  # WORKER进程数,通常为CPU数, 或 *2
