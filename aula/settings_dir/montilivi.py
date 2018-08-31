# This Python file uses the following encoding: utf-8
# Django settings for aula project.

from montilividev import *
location = lambda x: os.path.join(PROJECT_DIR, x)

TEMPLATES[0]['DIRS'] = [location('../montidemo/templates')]+TEMPLATES[0]['DIRS']

INSTALLED_APPS  = [
                    'aula.apps.presenciaSetmanal',
#                   'demo',
#                   'django.contrib.staticfiles',
                   ] + INSTALLED_APPS

NOM_CENTRE = 'INS Montilivi'
LOCALITAT = u"Girona"
URL_DJANGO_AULA = r'https://faltes.institutmontilivi.cat'

EMAIL_SUBJECT_PREFIX = '[DjangoFaltes Montilivi] '
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

STATICFILES_DIRS = [
    location( '../montidemo/static-web/'),
] + STATICFILES_DIRS

COMPRESS_ENABLED = False
