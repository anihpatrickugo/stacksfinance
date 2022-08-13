"""
Django settings for stacksfinance project.

Generated by 'django-admin startproject' using Django 3.2.5.

For more information on this file, see
https://docs.djangoproject.com/en/3.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.2/ref/settings/
"""
from cmath import e
import os
import django_heroku
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l+cs9_y#h449-#acu6b1rh4s9j8^xms%-$0h!g3sy%o0ut@p35'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ALLOWED_HOSTS = ['stacksfinance.herokuapp.com']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'crispy_forms',
    'anymail',
    
    'core.apps.CoreConfig',
]

CRISPY_TEMPLATE_PACK = 'bootstrap4'

SITE_ID = 1

ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
ACCOUNT_EMAIL_REQUIRED = True
ACCOUNT_EMAIL_UNIQUE = True
ACCOUNT_EMAIL_VERIFICATION = "optional"
ACCONT_LOGIN_ON_PASSWORD_RESET = True
DEFAULT_FROM_EMAIL = 'ugocee.pvu@gmail.com'


LOGIN_REDIRECT_URL = 'dashboard'
LOGOUT_REDIRECT_URL = 'home'

ACCOUNT_FORMS = {'signup': 'core.forms.SimpleSignupForm'}
AUTH_USER_MODEL = 'core.Profile'

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'stacksfinance.urls'

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


AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',

    'allauth.account.auth_backends.AuthenticationBackend',
]


WSGI_APPLICATION = 'stacksfinance.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'staticfiles')]
STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'



# media upload

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# email smtp settings

# EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'


# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_HOST = 'smtp.mail.yahoo.com'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = True
# EMAIL_PORT = 587
# EMAIL_HOST_USER = 'iampatrickugo@gmail.com'
# EMAIL_HOST_PASSWORD = 'Password_1999' 

# 1bb00ab446
# aa0997a8aa7530bef851a0fd00791293-us10

# EMAIL_BACKEND = 'django_mailjet.backends.MailjetBackend'
# EMAIL_HOST = 'in-v3.mailjet.com'
# MAILJET_API_KEY = 'd39cc2ecbab875ae2681df11b925fd58'
# MAILJET_API_SECRET = 'f8758e13b9ca950d6e519f96153338cf'
# EMAIL_PORT = '587'
# EMAIL_USE_TLS = True
# EMAIL_USE_SSL = False

# DEFAULT_FROM_EMAIL = 'ugochukwu <ugocee.pvu@gmail.com.'


# MAILCHIMP_API_KEY = 'aa0997a8aa7530bef851a0fd00791293-us10'
# MAILCHIMP_DATA_CENTER = 's10'
# MAILCHIMP_EMAIL_LIST_ID = '1bb00ab446'

EMAIL_BACKEND = 'anymail.backends.mailjet.EmailBackend'

ANYMAIL = {
    'MAILJET_API_KEY': 'd39cc2ecbab875ae2681df11b925fd58',
    'MAILJET_SECRET_KEY': 'f8758e13b9ca950d6e519f96153338cf',
}



# site settings

BITCOIN_ADDRESS = 'bc1qm0h7z8dy9wjn3n5yztn80n9fp4pjx2djmczzrx'
SITE_REFERRAL_BONUS = 10
MINIMUM_WITHDRAWAL_AMAOUNT = 5
WEBSITE_DEFAULT_SENDER_EMAIL = 'ugocee.pvu@gmail.com'
WEBSITE_ADMIN_EMAILS = ['iampatrickugo@gmail.com']



django_heroku.settings(locals())