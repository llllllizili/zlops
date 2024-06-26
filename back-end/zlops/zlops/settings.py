"""
Django settings for zlops project.

Generated by 'django-admin startproject' using Django 4.2.13.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

import os
from . import config
from pathlib import Path
from datetime import datetime, timedelta

# 邮件，接口信息等地方使用
SYS_NAME = "zlOps"
SYS_VERSION = "0.0.1"

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = config.SECRET_KEY
# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = config.DEBUG

ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    "daphne",
    "channels",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "django_celery_beat",
    "django_celery_results",
    "drf_yasg",
    "rest_framework",
    "django_filters",
    "apps.system",
    "apps.wf",
    "apps.ws",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "zlops.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": ["dist"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "zlops.wsgi.application"

# ASGI
ASGI_APPLICATION = "zlops.asgi.application"
CHANNEL_LAYERS = {
    "default": {
        "BACKEND": "channels_redis.core.RedisChannelLayer",
        "CONFIG": {
            "hosts": [
                "redis://{user}:{pwd}@{address}:{port}/{db}".format(
                    user=config.REDIS_USER,
                    pwd=config.REDIS_PASSWORD,
                    address=config.REDIS_ADDRESS,
                    port=config.REDIS_PORT,
                    db=config.REDIS_CHANNEL_DB,
                )
            ],
            "symmetric_encryption_keys": [SECRET_KEY],
            # "capacity": 1500,
            # "expiry": 10,
        },
    },
}

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": config.MYSQL_DB_NAME,
        "USER": config.MYSQL_DB_USER,
        "PASSWORD": config.MYSQL_DB_PASSWORD,
        "HOST": config.MYSQL_DB_HOST,
        "PORT": config.MYSQL_DB_PORT,
        "OPTIONS": {
            "autocommit": True,
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = "zh-hans"

TIME_ZONE = "Asia/Shanghai"

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "dist/static")
if DEBUG:
    STATIC_ROOT = None
    STATICFILES_DIRS = (os.path.join(BASE_DIR, "dist/static"),)

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

# 默认主键
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# restframework配置
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",
        "rest_framework.authentication.BasicAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
        "apps.system.permission.RbacPermission",
    ],
    "DEFAULT_RENDERER_CLASSES": [
        "utils.response.FitJSONRenderer",
        "rest_framework.renderers.BrowsableAPIRenderer",
    ],
    "DEFAULT_FILTER_BACKENDS": [
        "django_filters.rest_framework.DjangoFilterBackend",
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
    "DEFAULT_PAGINATION_CLASS": "utils.pagination.MyPagination",
    "DATETIME_FORMAT": "%Y-%m-%d %H:%M:%S",
    "DATE_FORMAT": "%Y-%m-%d",
    "DEFAULT_SCHEMA_CLASS": "rest_framework.schemas.coreapi.AutoSchema",
    "UNAUTHENTICATED_USER": None,
    "UNAUTHENTICATED_TOKEN": None,
}

# simple jwt
SIMPLE_JWT = {
    # 'ACCESS_TOKEN_LIFETIME': timedelta(days=1),
    "ACCESS_TOKEN_LIFETIME": timedelta(hours=24),
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),
    "AUTH_HEADER_TYPES": ("Bearer",),
}

# DRF 跨域   app: 'corsheaders',
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True
# CORS_ORIGIN_WHITELIST = ('*')
CORS_ALLOW_METHODS = (
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
    "VIEW",
)
CORS_ALLOW_HEADERS = (
    "XMLHttpRequest",
    "X_FILENAME",
    "accept-encoding",
    "authorization",
    "content-type",
    "dnt",
    "origin",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "Pragma",
    "x-token",
    "token",
)
# 邮箱配置
EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
EMAIL_HOST = config.EMAIL_HOST
EMAIL_PORT = config.EMAIL_PORT
EMAIL_HOST_USER = config.EMAIL_HOST_USER
EMAIL_HOST_PASSWORD = config.EMAIL_HOST_PASSWORD
EMAIL_USE_TLS = config.EMAIL_USE_TLS
SYSTEM_MANAGER_EMAIL = config.SYSTEM_MANAGER_EMAIL
DEFAULT_EMAIL_RECIPIENT = config.DEFAULT_EMAIL_RECIPIENT
# Auth配置
AUTH_USER_MODEL = "system.User"
AUTHENTICATION_BACKENDS = ("apps.system.authentication.CustomBackend",)

# 缓存设置（Redis）
CACHES = {
    "default": {
        "BACKEND": "django.core.cache.backends.redis.RedisCache",
        "LOCATION": "redis://{user}:{pwd}@{address}:{port}/{db}".format(
            user=config.REDIS_USER,
            pwd=config.REDIS_PASSWORD,
            address=config.REDIS_ADDRESS,
            port=config.REDIS_PORT,
            db=config.REDIS_CACHES_DB,
        ),
    }
}


# celery配置,celery正常运行必须安装redis
CELERY_BROKER_URL = "redis://{user}:{pwd}@{address}:{port}/{db}".format(
    user=config.REDIS_USER,
    pwd=config.REDIS_PASSWORD,
    address=config.REDIS_ADDRESS,
    port=config.REDIS_PORT,
    db=config.REDIS_CACHES_DB,
)  # 任务存储
CELERY_TASK_DEFAULT_QUEUE = config.BASE_PROJECT_CODE  # 任务队列
CELERYD_MAX_TASKS_PER_CHILD = (
    100  # 每个worker最多执行100个任务就会被销毁，可防止内存泄露
)
CELERY_TIMEZONE = "Asia/Shanghai"  # 设置时区
CELERY_ENABLE_UTC = True  # 启动时区设置
CELERY_RESULT_BACKEND = "django-db"
CELERY_BEAT_SCHEDULER = "django_celery_beat.schedulers:DatabaseScheduler"
CELERY_ACCEPT_CONTENT = ["application/json"]
CELERY_TASK_SERIALIZER = "json"
CELERY_RESULT_SERIALIZER = "json"
CELERY_RESULT_EXTENDED = True
CELERY_TASK_TRACK_STARTED = True
CELERYD_SOFT_TIME_LIMIT = 60 * 10
# WORKER_PREFETCH_MULTIPLIER = 20 # WORKER预取任务数量
CELERYD_CONCURRENCY = os.cpu_count() # WORKER进程数,通常为CPU数, 或 *2
CELERY_TASK_RESULT_EXPIRES = 60 * 60 * 24  # 结果存储有效时间
# 为 Celery 6.x 准备的配置
CELERY_BROKER_CONNECTION_RETRY_ON_STARTUP = True

# swagger配置
SWAGGER_SETTINGS = {
    "LOGIN_URL": "/swagger/login/",
    "LOGOUT_URL": "/swagger/logout/",
}


# 日志配置
# 创建日志的路径
LOG_PATH = os.path.join(BASE_DIR, "log")
# 如果地址不存在，则自动创建log文件夹
if not os.path.exists(LOG_PATH):
    os.makedirs(LOG_PATH)

LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "formatters": {
        # 日志格式
        "standard": {
            "format": "[%(asctime)s] [%(filename)s:%(lineno)d] [%(module)s:%(funcName)s] "
            "[%(levelname)s]- %(message)s"
        },
        "simple": {"format": "%(levelname)s %(message)s"},  # 简单格式
    },
    # 过滤
    "filters": {
        "require_debug_true": {
            "()": "django.utils.log.RequireDebugTrue",
        },
        'require_debug_false': {  # 和上面相反
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },
    # 定义具体处理日志的方式
    "handlers": {
        # 默认记录所有日志
        "default": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(
                LOG_PATH, "all-{}.log".format(datetime.now().strftime("%Y-%m-%d"))
            ),
            "maxBytes": 1024 * 1024 * 2,  # 文件大小
            "backupCount": 10,  # 备份数
            "formatter": "standard",  # 输出格式
            "encoding": "utf-8",  # 设置默认编码，否则打印出来汉字乱码
        },
        # 输出错误日志
        "error": {
            "level": "ERROR",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(
                LOG_PATH, "error-{}.log".format(datetime.now().strftime("%Y-%m-%d"))
            ),
            "maxBytes": 1024 * 1024 * 2,  # 文件大小
            "backupCount": 10,  # 备份数
            "formatter": "standard",  # 输出格式
            "encoding": "utf-8",  # 设置默认编码
        },
        # 控制台输出
        "console": {
            "level": "DEBUG",
            "class": "logging.StreamHandler",
            "filters": ["require_debug_true"],
            "formatter": "standard",
        },
        # 输出info日志
        "info": {
            "level": "INFO",
            "class": "logging.handlers.RotatingFileHandler",
            "filename": os.path.join(
                LOG_PATH, "info-{}.log".format(datetime.now().strftime("%Y-%m-%d"))
            ),
            "maxBytes": 1024 * 1024 * 2,
            "backupCount": 10,
            "formatter": "standard",
            "encoding": "utf-8",  # 设置默认编码
        },
    },
    # 配置用哪几种 handlers 来处理日志
    "loggers": {
        # 类型 为 django 处理所有类型的日志， 默认调用
        "django": {
            "handlers": ["default", "console"],
            "level": "INFO",
            "propagate": False,
        },
        # log 调用时需要当作参数传入
        "log": {
            "handlers": ["error", "info", "console", "default"],
            "level": "DEBUG",
            "propagate": True,
        },
    },
}
