from pathlib import Path
import os
from dotenv import load_dotenv

from firebase_admin import initialize_app, credentials

load_dotenv()
# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent



# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv('DEBUG')

ALLOWED_HOSTS = [os.getenv('ALLOWED_HOSTS')]


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django_cleanup.apps.CleanupConfig',
    #apps
    'apps.user',
    'apps.application',
    #others
    'corsheaders',
    'phonenumber_field',
    'django_filters',
    'rest_framework',
    'rest_framework.authtoken',
    'drf_yasg',
    'rest_registration',
    'fcm_django',
    'debug_toolbar',
    'celery',
    'ckeditor',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware'
]

ROOT_URLCONF = 'core.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        "DIRS": [BASE_DIR, "templates"],
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



DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    },
    'test': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': 'test_mydatabase',
    },
}


"""POSTGRES"""
# print( os.getenv('POSTGRES_DB'))
# DATABASES = {
#         'default': {
#             'ENGINE': 'django.db.backends.postgresql_psycopg2',
#             'NAME': os.getenv('POSTGRES_DB'),
#             'USER': os.getenv('POSTGRES_USER'),
#             'PASSWORD': os.getenv('POSTGRES_PASSWORD'),
#             'HOST': os.getenv('POSTGRES_HOST'),
#             'PORT': '',
#         }
#     }



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


PHONENUMBER_DB_FORMAT="INTERNATIONAL"

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Asia/Bishkek'


USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, "static", "static_root")
STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "static", "static_dirs"),
]
MEDIA_ROOT = os.path.join(BASE_DIR, "static", "media")
MEDIA_URL = '/media/'



DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.BasicAuthentication',
        'rest_framework.authentication.SessionAuthentication',
        'rest_framework.authentication.TokenAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': ['django_filters.rest_framework.DjangoFilterBackend'],
    'DEFAULT_PAGINATION_CLASS': 'api.pagination.StandardResultsSetPagination'
}


REST_REGISTRATION = {
    'LOGIN_RETRIEVE_TOKEN': True,
    'REGISTER_VERIFICATION_ENABLED': False,
    'REGISTER_EMAIL_VERIFICATION_ENABLED': False,
    'RESET_PASSWORD_VERIFICATION_ENABLED': False,
    'USER_LOGIN_FIELDS_UNIQUE_CHECK_ENABLED': True,
    'REGISTER_SERIALIZER_PASSWORD_CONFIRM':True,
    

    'USER_HIDDEN_FIELDS' : (
        'last_login',
        'is_active',
        'is_staff',
        'is_superuser',
        'user_permissions',
        'groups',
        'date_joined',
        'last_activity',
        'first_name',
        'last_name'    
    ),
    'REGISTER_SERIALIZER_CLASS':'apps.user.serializers.RegisterUserSerializer',
    'PROFILE_SERIALIZER_CLASS':'api.user.serializers.UserProfileSerializer',
}


CORS_ALLOWED_ORIGINS = [
    'http://localhost',
    'http://localhost:8000',
    'http://0.0.0.0:8000',
    'http://0.0.0.0:8001',
    'http://localhost:3000',
    'http://127.0.0.1',
    'http://127.0.0.1:3000',
    'http://0.0.0.0:8011',
    'http://localhost:8019'
    ]


CSRF_TRUSTED_ORIGINS = CORS_ALLOWED_ORIGINS


INTERNAL_IPS = [
    "127.0.0.1",
    "45.82.14.30"
]

USE_X_FORWARDED_HOST = True
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


LOGIN_URL = '/api/v1/accounts/login/'
LOGOUT_URL = '/api/v1/accounts/logout/'

AUTH_USER_MODEL = "user.User"


EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = os.getenv('EM_ACCOUNT')
EMAIL_HOST_PASSWORD = os.getenv('EM_PASSWORD')
EMAIL_PORT = 587
EMAIL_USE_TLS = True

DEF_PATH_KEY = '/Users/macpro2019/frilance/1c_applications-back/firebase_key.json'

cred = credentials.Certificate(os.getenv("DEF_PATH_KEY",DEF_PATH_KEY))
    
FIREBASE_APP = initialize_app(cred)

FCM_DJANGO_SETTINGS = {
    "DEFAULT_FIREBASE_APP": None,

    "APP_VERBOSE_NAME": 'Система уведомлении',

    "ONE_DEVICE_PER_USER": False,

    "DELETE_INACTIVE_DEVICES": False,
}


REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')


CELERY_BROKER_URL = f'redis://{REDIS_HOST}:6379/0'
CELERY_BROKER_TRANSPORT_OPTIONS = {'visibility_timeout': 3600}
CELERY_RESULT_BACKEND = f'redis://{REDIS_HOST}:6379/0'
CELERY_ACCEPT_CONTENT = ['application/json']
CELERY_TASK_SERIALIZER = 'json'
CELERY_RESULT_SERIALIZER = 'json'


NIKITA_SMPT_LOGIN = os.getenv('NIKITA_SMPT_LOGIN')
NIKITA_SMPT_PASSWORD = os.getenv('NIKITA_SMPT_PASSWORD')
NIKITA_SMPT_STATUS = os.getenv('NIKITA_SMPT_STATUS')
NIKITA_SMPT_SENDER_NAME = os.getenv('NIKITA_SMPT_SENDER_NAME')


CKEDITOR_UPLOAD_PATH = 'uploads/'
CKEDITOR_IMAGE_BACKEND = "pillow"
CKEDITOR_JQUERY_URL = '//ajax.googleapis.com/ajax/libs/jquery/2.1.1/jquery.min.js' 

CKEDITOR_CONFIGS = {
    'default':
        {
            'height': 150,
            'width': 'full', 
                'extraPlugins': ','.join([
                    'codesnippet',
            ]),
        },
}
