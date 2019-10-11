"""
Django settings for mysite project.

Generated by 'django-admin startproject' using Django 2.0.

For more information on this file, see
https://docs.djangoproject.com/en/2.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.0/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'piws#a^f6w+!7q4phx*bu8a@-n=p105sp)dkkmal8*+do&4qs2'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'ckeditor',
    'ckeditor_uploader',
    'blog',
    'read_statistics',
    'comment',
    
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'mysite.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            os.path.join(BASE_DIR, 'templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'mysite.wsgi.application'


# Database
# https://docs.djangoproject.com/en/2.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'mysite',
        'USER': 'postgres',
        'PASSWORD': '941128',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}


# Password validation
# https://docs.djangoproject.com/en/2.0/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.0/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

USE_TZ = False  # True改为False, 否则Django存储数据库内容时, 会使用UTC时间.


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.0/howto/static-files/

# 设置静态文件的起始路由，无论这里设置成什么名字，寻找时都会从"STATICFILES_DIRS"开始寻找
# 例如htts://localhost:8000/static/....
# http://localhost:8000/file/....   STATIC_URL = 'file'
STATIC_URL = '/static/'
# 所有静态文件都会从这里的目录开始寻找
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static'),
]
# media 配置
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')
# ckeditor 配置
CKEDITOR_UPLOAD_PATH = 'upload/'
# 日志
LOG_PATH = os.path.join(BASE_DIR, 'log')
# 如果日志文件夹不存在，则创建
if not os.path.isdir(LOG_PATH):
    os.mkdir(LOG_PATH)
# 配置
LOGGING = {
    'version': 1,  # 指明dictConnfig的版本，目前就只有一个版本
    'disable_existing_loggers': False,  # 表示是否禁用所有的已经存在的日志配置
    # 指定输出格式
    'formatters': {
        'verbose': {  # 详细
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
        'simple': {  # 标准
            'format': '%(levelname)s %(message)s'
        },
    },
    # handlers：用来定义具体处理日志的方式
    'handlers': { # 处理器
        'stu_handlers': {
            # 如果loggers的处理级别小于handlers的级别，则handler忽略该消息
            'level':'DEBUG',
            # 指定文件类型，当日志文件的大小超过了maxbytes时，会自动进行分割
            'class':'logging.handlers.RotatingFileHandler',
            # 日志输出文件
            'filename': '%s/log.txt' % LOG_PATH,
            # 文件大小
            'maxBytes': 1024*1024*5,
            # 使用哪种formatters日志格式
            'formatter':'verbose',                   
        },
    },
    # log记录器，配置之后就会对应的输出日志,loggers的level的级别一定要大于handlers的级别，否则handlers会忽略掉该信息的
    'loggers': {
        'console': {
            'handlers': ['stu_handlers'],
            'level': 'INFO',
            'propagate': False,
        },
    },
}
# 自定义常量
EACH_PAGE_BLOGS_NUMBER = 6 # 每页博客数量