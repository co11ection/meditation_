import os
import environ
from pathlib import Path

from django.template.context_processors import media

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "omtogether.settings")

BASE_DIR = Path(__file__).resolve().parent.parent
env = environ.Env()
environ.Env.read_env()

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = env.str('SECRET_KEY')
DEBUG = env.bool('DEBUG', default=False)
ALLOWED_HOSTS = env.list("ALLOWED_HOSTS")

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'users.apps.UsersConfig',
    'onboarding.apps.OnboardingConfig',
    'meditacia.apps.MeditaciaConfig',
    'wallet.apps.WalletConfig',

    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',

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

ROOT_URLCONF = 'omtogether.urls'
TEMPLATES_DIR = BASE_DIR / 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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

WSGI_APPLICATION = 'omtogether.wsgi.application'

# Database
# https://docs.djangoproject.com/en/3.2/ref/settings/#databases

DATABASES = {
    'default': env.db()
}
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.postgresql',
#         'NAME': 'omtogether',
#         'USER': 'postgres',
#         'PASSWORD': '12345',
#         'HOST': 'db',
#         # Здесь используйте имя сервиса из docker-compose.yml
#         'PORT': '5432',
#     }
# }

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

EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = env.str("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = env.str("EMAIL_HOST_PASSWORD")

SMS_LOGIN = env.str("SMS_LOGIN")
SMS_PASSWORD = env.str("SMS_PASSWORD")

# Internationalization
# https://docs.djangoproject.com/en/3.2/topics/i18n/

LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.2/howto/static-files/

MEDIA_URL = ''

MEDIA_ROOT = BASE_DIR / 'media/'

STATIC_URL = '/static/'

STATIC_ROOT = BASE_DIR / 'static/'

# STATIC_ROOT = os.path.join(BASE_DIR, 'static')

# Default primary key field type
# https://docs.djangoproject.com/en/3.2/ref/settings/#default-auto-field

AUTH_USER_MODEL = 'users.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'rest_framework.schemas.coreapi.AutoSchema',
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.AllowAny',
    ],
}


CELERY_BROKER_URL = 'redis://localhost:6379/0'  # Используйте свои параметры подключения к брокеру
CELERY_RESULT_BACKEND = 'redis://localhost:6379/1'  # Используйте свои параметры
