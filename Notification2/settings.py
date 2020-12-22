import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_KEY = 'dc=wn$q$whc7i4sim-!*=$aawo%3*%-zau29+j&)g4s(pe4b@t'
DEBUG = True
PYTHON_ANY_WHERE=False
if PYTHON_ANY_WHERE:
    ALLOWED_HOSTS = ['godod4.pythonanywhere.com']
else:
    ALLOWED_HOSTS = ['localhost']


from django.conf.global_settings import DATETIME_INPUT_FORMATS
DATETIME_INPUT_FORMATS += ('%Y-%m-%dT%H:%M:%S',) #https://docs.djangoproject.com/en/2.2/ref/settings/#datetime-input-formats

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    "Act",
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
ROOT_URLCONF = 'Notification2.urls'

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
WSGI_APPLICATION = 'Notification2.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'Europe/Moscow'



if PYTHON_ANY_WHERE:
    STATIC_URL = '/static/'
    MEDIA_ROOT = '/home/godod4/dj_project/media'
    MEDIA_URL = '/media/'
    STATIC_ROOT = '/home/godod4/dj_project/static'
else:
    MEDIA_ROOT = r'C:\Users\prog2.HLEB\Desktop\Нужное\p\ProjectVs\SystemNotification/media'
    MEDIA_URL = '/media/'
    STATIC_ROOT = r'C:\Users\prog2.HLEB\Desktop\Нужное\p\ProjectVs\SystemNotification/static'
    STATIC_URL = '/static/'

