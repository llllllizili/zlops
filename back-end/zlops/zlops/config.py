#!/usr/bin python
# -*- encoding: utf-8 -*-
'''
@File    :    config.py
@Time    :   2024/06/03 08:42:25
'''

# 基本配置
SECRET_KEY = 'sk2lw67kei6cdmno'
BASE_PROJECT_CODE = 'zlops'  # 一旦配置不要变
REDIS_CACHES_DB = 1
REDIS_CELERY_BROKER_DB = 2
CREATE_USER_DEFAULT_PASSWORD = '123456' # 为设置密码时候，默认密码

# 邮箱配置
EMAIL_HOST = 'xx'
EMAIL_PORT = 25
EMAIL_HOST_USER = 'xx'
EMAIL_HOST_PASSWORD = 'xx'
EMAIL_USE_TLS = True

# 数据库
DEBUG = True
DATABASES = {
    'default': {
         'ENGINE': 'django.db.backends.mysql',
         'NAME': 'zlops',
         'USER': 'root',
         'PASSWORD': 'Password_1',
         'HOST': '127.0.0.1',
         'PORT': '3306',
         'OPTIONS': {
            'autocommit': True,
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}
# Redis缓存配置
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://default:123qweASD@127.0.0.1:6379/{db}".format(db=REDIS_CACHES_DB),
    }
}

# celery
CELERY_BROKER_URL = "redis://127.0.0.1:6379/{db}".format(db=REDIS_CELERY_BROKER_DB)
CELERY_TASK_DEFAULT_QUEUE = BASE_PROJECT_CODE
CELERY_WORKER_CONCURRENCY = 4 # WORKER进程数,通常为CPU数, 或 *2

