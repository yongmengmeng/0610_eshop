"""
Django settings for eshop project.

Generated by 'django-admin startproject' using Django 2.1.8.

For more information on this file, see
https://docs.djangoproject.com/en/2.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/2.1/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'slo!46)kdf7%2+i_o&0oi)o(d3fhgsg2pp8^wq-%!idulcs2e3'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'store',
    'ckeditor',
    'ckeditor_uploader',
    'buyer',
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

ROOT_URLCONF = 'eshop.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'eshop.wsgi.application'

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'my_eshop',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '10.10.2.160',
        # 'HOST': '10.10.9.197',
        'PORT': '3306',
    }
}

# Password validation
# https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/2.1/topics/i18n/

LANGUAGE_CODE = 'en-us'

# 设置时间
TIME_ZONE = 'Asia/Shanghai'

USE_I18N = True

USE_L10N = True

# 设置时间
USE_TZ = False

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/2.1/howto/static-files/

# 设置静态文件的路由
STATIC_URL = '/static/'
# 配置静态文件所在的目录
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, 'static')
]
# 设置文件上传的url
MEDIA_URL = '/static/media/'
# 设置文件上传的位置
MEDIA_ROOT = os.path.join(BASE_DIR, 'static/media')
# 设置django-ckeditor
CKEDITOR_UPLOAD_PATH = 'upload'
CKEDITOR_IMAGE_BACKEDND = 'pillow'
# 设置收集静态文件的路径
# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

#################用户认证系统#################
# 1、登录url
LOGIN_URL = '/buyer/login/'
# 2、用户模块
AUTH_USER_MODEL = 'buyer.Buyer'
# 3、验证用户，比如登录
AUTHENTICATION_BACKENDS = ['django.contrib.auth.backends.AllowAllUsersModelBackend']

#################配置发送邮件#################
# 1、django中的发邮件的管理类
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# 2、smtp服务器
EMAIL_HOST = 'smtp.126.com'
# 3、smtp服务器端口号
EMAIL_PORT = 25
# 4、发送邮件的邮箱
EMAIL_HOST_USER = 'gebidaxiaowang@126.com'
# 5、在邮箱中设置的客户端授权密码
EMAIL_HOST_PASSWORD = '1807bb'
# 6、# 收件人看到的发件人信息
EMAIL_FROM = '天天生鲜<gebidaxiaowang@126.com>'
