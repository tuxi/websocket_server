"""
Django settings for websocket_server project.

Generated by 'django-admin startproject' using Django 1.11.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

import os
import sys
from websocket_server.private_config import YUNPIAN_APIKEY

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, 'apps'))
sys.path.insert(0, os.path.join(BASE_DIR, 'extra_apps'))



# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&ds85fwdgh&r&e2*7xnfcmvva(s@h*%5r39+aau&8o!w^!0mjg'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True
AUTH_USER_MODEL = 'users.UserProfile'
ALLOWED_HOSTS = ["*"]


# Application definition

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'corsheaders', # 跨域访问 解决
]

EXTRA_APPS = [
    'xadmin',
    'DjangoUeditor',
    'django_filters',
    'crispy_forms',
    'rest_framework',
    'rest_framework.authtoken',  # 用户登录
    'gunicorn',
]

PERSONAL_APPS = [
    'users.apps.UsersConfig',
    'pinax.likes.apps.AppConfig',
]

INSTALLED_APPS += PERSONAL_APPS + EXTRA_APPS

MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# 必须跟原域匹配才可获取发送 cookie 的权限
CORS_ORIGIN_REGEX_WHITELIST = r'.*'
# 必须有这个才接受前端跨域发送 cookie
CORS_ALLOW_CREDENTIALS = True
CORS_ORIGIN_ALLOW_ALL = True

# 允许所有的请求头
CORS_ALLOW_HEADERS = (' * ')

ROOT_URLCONF = 'websocket_server.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'django.template.context_processors.media',  # 用于在模板中使用{{MEDIA_URL}}
            ],
        },
    },
]


WSGI_APPLICATION = 'websocket_server.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.11/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}


# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/1.11/topics/i18n/
#设置时区
LANGUAGE_CODE = 'zh-hans'  #中文支持，django1.8以后支持；1.8以前是zh-cn
TIME_ZONE = 'Asia/Shanghai'
USE_I18N = True
USE_L10N = True
USE_TZ = False   #默认是Ture，时间是utc时间，由于我们要用本地时间，所用手动修改为false！！！！

AUTHENTICATION_BACKENDS = (
    # 使用自定义的用户验证, 用户登录时调用 users.views.CustomBackend验证
    'users.views.CustomBackend',
    'pinax.likes.auth_backends.CanLikeBackend',
)


import datetime
JWT_AUTH = {
    # JWT过期时间
    'JWT_EXPIRATION_DELTA': datetime.timedelta(days=7),
    # 需要前端在request 的 headers 中 为JWT，只要前后端相同即可
    'JWT_AUTH_HEADER_PREFIX': 'JWT',
    # 自定义jwt返回数据 编写返回的数据, 这里把user和token同时返回给客户端
    'JWT_RESPONSE_PAYLOAD_HANDLER':'users.views.jwt_response_payload_handler',
}


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        # 全局配置 将用户请求的数据进行验证，将user取出来
        # 不需要全局配置，在需要的地方配置
       # 'rest_framework_jwt.authentication.JSONWebTokenAuthentication',
    )
}




# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/


STATIC_URL = '/static/'
# 部署的时候注释掉，不然无法执行collecstatic命令，运行时打开
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]

# 部署时收集静态文件collecstatic需要的目录配置，部署完成后注释掉，不然debug下报错无法读取static下的文件
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = "/media/"


MEDIA_ROOT = os.path.join(BASE_DIR, "media")

#手机号码正则表达式
REGEX_MOBILE = "^1[358]\d{9}$|^147\d{8}$|^176\d{8}$"

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

# pinax likes app config
PINAX_LIKES_LIKABLE_MODELS = {
    "users.UserProfile": {
            "like_text_on": "unlike",
            # "css_class_on": "fa-heart",
            "like_text_off": "like",
            # "css_class_off": "fa-heart-o",
            "allowed": lambda user, obj: True
        },
}
