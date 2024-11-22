"""
Django settings for doctor project.

Generated by 'django-admin startproject' using Django 4.2.16.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.2/ref/settings/
"""

from pathlib import Path
import os
from dotenv import load_dotenv
# Cargar las variables de entorno desde el archivo .env
load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('SECRET_KEY')

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
    # apps de usuarios
    'aplication.core.apps.CoreConfig',
    'aplication.attention.apps.AttentionConfig',
    'aplication.security.apps.SecurityConfig',
    # apps de terceros
    'django_extensions',
    'widget_tweaks',
   

]
SHELL_PLUS = "ipython"  # Si tienes IPython instalado, usa esta opción
SHELL_PLUS_PRINT_SQL = True

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'doctor.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'template')],
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

WSGI_APPLICATION = 'doctor.wsgi.application'



AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',  # Este es el backend por defecto
)

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases

DATABASES = {
    "default": {
        'ENGINE': os.environ.get("DB_ENGINE", "django.db.backends.postgresql"),
        'NAME': os.environ.get("DB_DATABASE", ""),
        'USER': os.environ.get("DB_USERNAME", ""),
        'PASSWORD': os.environ.get("DB_PASSWORD", ""),
        'HOST': os.environ.get("DB_SOCKET", ""),
        'PORT': os.environ.get("DB_PORT", "5432"),
        'ATOMIC_REQUESTS': True
    }
}

# Password validation
# https://docs.djangoproject.com/en/4.2/ref/settings/#auth-password-validators

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
# https://docs.djangoproject.com/en/4.2/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.2/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')
STATICFILES_DIRS = (os.path.join(BASE_DIR, 'static'),)#carpeta fisica de archivos estaticos
MEDIA_ROOT = os.path.join(BASE_DIR,'media') # carpeta fisica de archivos de Imagenes
MEDIA_URL = '/media/' # 

AUTH_USER_MODEL = 'security.User'

SESSION_ENGINE = 'django.contrib.sessions.backends.db'  # Usar base de datos para sesiones
SESSION_COOKIE_AGE = 3600

# Login 
LOGIN_URL = 'security:auth_login'  # O la URL que hayas configurado para el login

# Si un usuario intenta acceder a una página que requiere autenticación
# y no está autenticado, lo redirigirá a la página de login.
LOGIN_REDIRECT_URL = 'security:modules_list'  

# Si la autenticación se realiza correctamente, usa esta URL para redirigir:
LOGOUT_REDIRECT_URL = 'core:home'

# Default primary key field type
# https://docs.djangoproject.com/en/4.2/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Configuración de envío de correos electrónicos
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = os.environ.get("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.environ.get("EMAIL_HOST_PASSWORD")
DEFAULT_FROM_EMAIL = EMAIL_HOST_USER

PAYPAL_CLIENT_ID = os.environ.get("PAYPAL_CLIENT_ID")
PAYPAL_SECRET = os.environ.get("PAYPAL_SECRET")