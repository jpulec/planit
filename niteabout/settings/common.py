# Django settings for niteabout project.
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

ADMINS = (
     ('James Pulec', 'jpulec@gmail.com'),
)

MANAGERS = ADMINS

DATABASES = {
        'default':
            {
                'ENGINE': 'django.contrib.gis.db.backends.postgis',
                'NAME': os.environ['POSTGRESQL_NAME'],
                'USER': os.environ['POSTGRESQL_USERNAME'],
                'PASSWORD': os.environ['POSTGRESQL_PASSWORD'],
                'HOST': os.environ['POSTGRESQL_HOST'],
                'PORT': os.environ['POSTGRESQL_PORT'],
            }
    }

# Local time zone for this installation. Choices can be found here:
# http://en.wikipedia.org/wiki/List_of_tz_zones_by_name
# although not all choices may be available on all operating systems.
# In a Windows environment this must be set to your system time zone.
TIME_ZONE = 'America/Chicago'

# Language code for this installation. All choices can be found here:
# http://www.i18nguy.com/unicode/language-identifiers.html
LANGUAGE_CODE = 'en-us'

# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

# Additional locations of static files
STATICFILES_DIRS = (
        os.path.join(BASE_DIR, 'static'),
)

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = os.environ['SECRET_KEY']

# List of callables that know how to import templates from various sources.
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
#     'django.template.loaders.eggs.Loader',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
    'django.core.context_processors.static',
    'django.core.context_processors.tz',
    'django.core.context_processors.i18n',
    'django.contrib.messages.context_processors.messages',
    #'niteabout.apps.business.context_processors.add_business',
    )

MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # Uncomment the next line for simple clickjacking protection:
    #'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'niteabout.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'niteabout.wsgi.application'

TEMPLATE_DIRS = (os.path.join(BASE_DIR, 'templates'),
    # Put strings here, like "/home/html/django_templates" or "C:/www/django/templates".
    # Always use forward slashes, even on Windows.
    # Don't forget to use absolute paths, not relative paths.
)

INSTALLED_APPS = (
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.admin',
    'django.contrib.gis',
    'djangoratings',
    'south',
    'mathfilters',
    'registration',
    'organizations',
    'niteabout.apps.main',
    'niteabout.apps.events',
    'niteabout.apps.gatherer',
    'niteabout.apps.plan',
    'niteabout.apps.places',
    'niteabout.apps.movies',
    'niteabout.apps.business',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    "formatters": {
        "verbose": {
            "format": "%(levelname)s %(asctime)s %(module)s %(process)d %(thread)s %(message)s"
            },
        "simple": {
            "format": "%(levelname)s %(message)s"
            },
        },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'null': {
            'level':'DEBUG',
            'class': 'logging.NullHandler',
            },
        'console': {
            'level': 'DEBUG',
            'class': "logging.StreamHandler",
            'formatter': 'simple'
            },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'filename': os.path.join(BASE_DIR,'../../logs/django.log'),
            'mode': 'a',
            'maxBytes': '10485760',
            'backupCount': 5,
            },
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'sentry': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'raven.contrib.django.handlers.SentryHandler',
            },
    },
    'loggers': {
        'django': {
            'handlers': ['file', 'sentry'],
            'propagate': True,
            'level' : 'DEBUG',
            },
        'niteabout': {
            'handlers': ['file', 'sentry'],
            "level": 'DEBUG',
            "propagate": True
            },
    }
}

TIME_INPUT_FORMATS = ['%H:%M', '%I:%M%p', '%I:%M %p']

ACCOUNT_ACTIVATION_DAYS = 2
