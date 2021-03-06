#coding:utf-8
"""
Django settings for shannon project.

Generated by 'django-admin startproject' using Django 1.10.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os
HAYSTACK_CONNECTIONS = {
    'default':{
        'ENGINE': 'haystack.backends.whoosh_cn_backend.WhooshEngine',
        'PATH': os.path.join(os.path.dirname(__file__), 'whoosh_index'),
        },
    }

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = ''

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

#ALLOWED_HOSTS = ['*']
ALLOWED_HOSTS = ['127.0.0.1', 'localhost']
# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth', #contains the core of the authentication framework, and its default models.
    'django.contrib.contenttypes',  #is the Django content type system, which allows permissions to be associated with models you create
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'ccposts',
    'ccusers',
    'comments',
    'whoosh',
    'haystack',
    'pagedown',
    'markdown',
    'pygments',
    'taggit',
    'markdown_deux',
    'jquery',
    'jquery_ui',
    'bootstrap',
    'crispy_forms',
    'rest_framework',
    'secretballot',
    'cclikes',
    'schedule',
]

CRISPY_TEMPLATE_PACK = 'bootstrap3'

SITE_ID = 1

REST_FRAMEWORK = {
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAdminUser',
    ],
   # 'PAGE_SIZE': 10 #default pagination
}

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',#manages sessions across requests.
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',#associates users with requests using sessions.
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'secretballot.middleware.SecretBallotIpUseragentMiddleware',
    'cclikes.middleware.SecretBallotUserIpUseragentMiddleware',
]

ROOT_URLCONF = 'shannon.urls'


TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
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

WSGI_APPLICATION = 'shannon.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',#mysql',#sqlite3',
        'NAME': '#',
        'USER': '#',
        'PASSWORD': '#',
        'HOST': '127.0.0.1',
        'PORT': '5432',#'3306',
    }
}

WHOOSH_INDEX = os.path.join(BASE_DIR, 'whoosh/')
HAYSTACK_CONNECTION = {
    'default': {
        'ENGINE' : 'ccposts.whoosh_cn_backend.WhooshEngine',
        #'ENGINE': 'haystack.backends.whoosh_backend.WhooshEngine',
        'PATH': WHOOSH_INDEX,
    }
}

HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'




#SESSION_ENGINE = 'django.contrib.sessions.backends.db'
#SESSION_COOKIE_SECURE = False


# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators
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
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGE_CODE = 'zh-hans'

TIME_ZONE = 'Asia/Shanghai' #'UTC'
#If you want to make it your local timezone, go check on
#https://en.wikipedia.org/wiki/List_of_tz_database_time_zones
#other settings on https://docs.djangoproject.com/en/1.10/topics/i18n/timezones/

USE_I18N = True
USE_L10N = True
USE_TZ = True

#static_url
# https://docs.djangoproject.com/en/1.10/howto/static-files/
STATIC_URL = '/static/'


PASSWORD_HASHERS =(
    'django.contrib.auth.hashers.PBKDF2PasswordHasher',
    'django.contrib.auth.hashers.PBKDF2SHA1PasswordHasher',
    'django.contrib.auth.hashers.Argon2PasswordHasher',
    'django.contrib.auth.hashers.BCryptSHA256PasswordHasher',
    'django.contrib.auth.hashers.BCryptPasswordHasher',
    )


SIGNING_BACKEND = 'django.core.signing.TimestampSigner'

REGISTRATION_OPEN = True
#If True, users can register

ACCOUNT_ACTIVATION_DAYS = 7# One-week activation window; you may, of course, use a different value.
REGISTRATION_AUTO_LOGIN = True# If True, the user will be automatically logged in.

AUTH_USER_MODEL = 'ccusers.MyUser'
#LOGIN_REDIRECT_URL = '/ccposts/' # The page you want users to arrive at after they successful log in
#LOGIN_URL = '/accounts/login/'# The page users are directed to if they are not logged in,


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
#EMAIL_HOST = 'smtp.qq.com'  #SMTP地址
EMAIL_HOST = 'localhost'
EMAIL_PORT = 1025
#The two for email local test! To start the local server,
#you should add "python -m smtpd -n -c DebuggingServer localhost:1025" in admin cmd.

#EMAIL_HOST_USER = '#'
#EMAIL_HOST_PASSWORD = '#'
#EMAIL_SUBJECT_PREFIX = '#'

#EMAIL_USE_TLS = True
#EMAIL_USE_SSL = True

#DEFAULT_FROM_EMAIL = '#'
#To send a real mail when making a password reset request, better add this default_from_mail.
#However, after a bunch of tests, I find that there is no need to do so when need to send register activation email.
#haven't figured out why so, perhaps because I achieve the register and login function by myself,
#while use the django.contrib.auth.view to achieve the password rest part???