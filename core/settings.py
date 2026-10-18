import os
from pathlib import Path
from datetime import timedelta
from decouple import config, Csv
import dj_database_url

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Security and Debug
SECRET_KEY = config(
    'SECRET_KEY',
    default='django-insecure-simple-app-template-key-change-in-production-!@#$'
)
DEBUG = config('DEBUG', default=True, cast=bool)
ALLOWED_HOSTS = config('ALLOWED_HOSTS', default='*', cast=Csv())

# Application definition
INSTALLED_APPS = [
    # Django Built-in Apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # Third-Party Apps
    'corsheaders',
    'rest_framework',
    'rest_framework_simplejwt',
    'drf_spectacular',

    # Local Project Apps
    'apps.common',
    'apps.users',
    'apps.authentication',
]

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

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'templates'],
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

WSGI_APPLICATION = 'core.wsgi.application'
ASGI_APPLICATION = 'core.asgi.application'

# Database Configuration (SQLite default; PostgreSQL ready via DATABASE_URL)
DATABASE_URL = config('DATABASE_URL', default=f"sqlite:///{BASE_DIR / 'dev.db'}")
DATABASES = {
    'default': dj_database_url.parse(
        DATABASE_URL,
        conn_max_age=600,
        conn_health_checks=True
    )
}

# Custom User Model
AUTH_USER_MODEL = 'users.User'

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6}},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# Static and Media files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# CORS Headers
CORS_ALLOW_ALL_ORIGINS = config('CORS_ALLOW_ALL_ORIGINS', default=True, cast=bool)
CORS_ALLOW_CREDENTIALS = True

# Django REST Framework
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'apps.common.authentication.ApiKeyAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ),
    'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.IsAuthenticated',
    ),
    'DEFAULT_PAGINATION_CLASS': 'apps.common.pagination.StandardResultsSetPagination',
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'EXCEPTION_HANDLER': 'apps.common.exceptions.custom_exception_handler',
}

# SimpleJWT Settings
JWT_PRIVATE_KEY = config(
    'JWT_PRIVATE_KEY',
    default='b9870e9725b03e83d7180a49b018011b31d59fbf7460806a1e0550f55b5135ba64264032deb23c5ffaf0e1a932e76f0df9f8f402275f61d49c3c4aa9d832131b'
)

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=config('ACCESS_SIGN_DAYS', default=7, cast=int)),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=config('REFRESH_SIGN_DAYS', default=30, cast=int)),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': False,
    'UPDATE_LAST_LOGIN': True,
    'SIGNING_KEY': JWT_PRIVATE_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Spectacular (OpenAPI 3.0 / Swagger UI)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Simple App Django API',
    'DESCRIPTION': 'Template completo de API backend com Django REST Framework, Django Admin, JWT e Autenticação por Chave de API.',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'persistAuthorization': True,
        'displayOperationId': False,
    },
}

# AES-256-CBC Encryption Settings (Used for API Keys)
ENCRYPTION_ALGORITHM = config('ENCRYPTION_ALGORITHM', default='aes-256-cbc')
ENCRYPTION_KEY = config('ENCRYPTION_KEY', default='305b4d83eae2e3e00484336539a8ecd29c841a86f1087e5768cf4f09344266f6')
ENCRYPTION_IV = config('ENCRYPTION_IV', default='18859ed3ccba5ece96c6f7fb3edf3b94')

# Default Admin Credentials for `seed_admin`
ADMIN_DEFAULT_USERNAME = config('ADMIN_DEFAULT_USERNAME', default='admin')
ADMIN_DEFAULT_EMAIL = config('ADMIN_DEFAULT_EMAIL', default='admin@email.com')
ADMIN_DEFAULT_NAME = config('ADMIN_DEFAULT_NAME', default='Admin')
ADMIN_DEFAULT_PASSWORD = config('ADMIN_DEFAULT_PASSWORD', default='DVbOwTVuszzkCcZ1cB9RiSIzSHaPdWZo')
ADMIN_DEFAULT_API_KEY = config(
    'ADMIN_DEFAULT_API_KEY',
    default='adm_19b7bb01a40ebf40789f23296ed348aed9ef161caa3634f1f0f8892151c10b4d'
)
