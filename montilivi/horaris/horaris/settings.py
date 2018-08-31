# Django settings for horaris project.
import os

# Django settings for aula project.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEBUG = True

###################################
# Produccio vs Desenvolupament
###################################

if not DEBUG:
    # Hosts/domain names that are valid for this site; required if DEBUG is False
    # See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
    ALLOWED_HOSTS = ['localhost', 'horaris.faltes.iesmontilivi.net:8008', 'horaris.faltes:8008']

###################################
# Altres
###################################

ADMINS = (
    ('root', 'xeviterr@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql', # Add 'postgresql_psycopg2', 'mysql', 'sqlite3' or 'oracle'.
        'NAME': 'gitdjangohoraris',                      # Or path to database file if using sqlite3.
        # The following settings are not used with sqlite3:
        'USER': 'userdjangohoraris',
        'PASSWORD': 'patata',
        'HOST': '',                      # Empty for localhost through domain sockets or '127.0.0.1' for localhost through TCP.
        'PORT': '',                      # Set to empty string for default.
    }
}

# Hosts/domain names that are valid for this site; required if DEBUG is False
# See https://docs.djangoproject.com/en/1.5/ref/settings/#allowed-hosts
ALLOWED_HOSTS = []

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

SITE_ID = 1

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/var/www/example.com/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "media")

# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/var/www/example.com/static/"
STATIC_ROOT = ''

# Additional locations of static files
STATICFILES_DIRS = (
    # Put strings here, like "/home/html/static" or "C:/www/django/static".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
    os.path.join(BASE_DIR, "static"),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = 'xhek)13t@91=nj-d0u-9i75#=c6n4hlmrljq*9b#k5*s363cjd'

# List of callables that know how to import templates from various sources.
#TEMPLATE_LOADERS = (
#    'django.template.loaders.filesystem.Loader',
#    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
#)

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',

    # Uncomment the next line for simple clickjacking protection:
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'horaris.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'horaris.wsgi.application'

#TEMPLATE_DIRS = (
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
#    os.path.join(BASE_DIR, "templates"),
#)

INSTALLED_APPS = [
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'extHoraris',
    'accounts'
]

SESSION_SERIALIZER = 'django.contrib.sessions.serializers.JSONSerializer'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': '/tmp/errorDjangoHoraris.log',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

TMP_DIR = os.path.join(BASE_DIR, "tmp")

EXT_HORARIS_DIR = os.path.join(BASE_DIR, '../extHoraris/xls/')

'''
Canviar l'aplicacio de horaris per tal que funcioni sobre el subdirectori horaris.

http://stackoverflow.com/questions/3232349/multiple-instances-of-django-on-a-single-domain

'''
URL_PREFIX = '/'
STATIC_URL = '/static/'
# Veure documentacio punt 4_15 manual oficial, explica el funcionament de media.
MEDIA_URL = '/media/'
ADMIN_MEDIA_PREFIX = '/admin_media/'

#Per fer subdominis
#Importantissim el COOKIE_DOMAIN per evitar conflictes amb les variables de sessio.
#SESSION_COOKIE_PATH = '/horaris'
#SESSION_COOKIE_PATH = '/horaris'
#LOGIN_REDIRECT_URL = '/horaris/'
#LOGIN_URL = '/horaris/accounts/login/'
#LOGOUT_URL = '/horaris/accounts/logout/'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, "templates")],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': DEBUG,
            'context_processors': ['django.contrib.auth.context_processors.auth'],
            # ... some options here ...
        },
    },
]
