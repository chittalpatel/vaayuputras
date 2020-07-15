import os
# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.11/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = '+)!83krz^m$i%=uo!4b7ps2s7q=2ikcm#sw!c=#6v9er#hx8or'


ALLOWED_HOSTS = ['*']


# Application definition
INSTALLED_APPS = [
                  'django.contrib.admin',
                  'django.contrib.auth',
                  'django.contrib.contenttypes',
                  'django.contrib.sessions',
                  'django.contrib.messages',
                  'django.contrib.staticfiles',
                  'django.contrib.flatpages',
                  'django.contrib.redirects',
                  'django.contrib.sites',
                  'rest_framework',
                  'rest_framework.authtoken',

    # all auth
                  'allauth',
                  'allauth.account',
                  'allauth.socialaccount',

    # providers
                  'allauth.socialaccount.providers.google',
                  'allauth.socialaccount.providers.facebook',
                  'allauth.socialaccount.providers.twitter',
                  'livereload',
                  'app',
                  'api',
                  'django.contrib.admindocs',
                  ]

MIDDLEWARE = [
              'django.middleware.security.SecurityMiddleware',
              'whitenoise.middleware.WhiteNoiseMiddleware',
              'django.contrib.sessions.middleware.SessionMiddleware',
              'django.middleware.common.CommonMiddleware',
              'django.middleware.csrf.CsrfViewMiddleware',
              'django.contrib.auth.middleware.AuthenticationMiddleware',
              'django.contrib.messages.middleware.MessageMiddleware',
              'django.middleware.clickjacking.XFrameOptionsMiddleware',
              ]


ROOT_URLCONF = 'pythondjangoapp.urls'

TEMPLATES = [
             {
             'BACKEND': 'django.template.backends.django.DjangoTemplates',
             'DIRS': [os.path.join(BASE_DIR, 'app', 'templates')],
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

WSGI_APPLICATION = 'pythondjangoapp.wsgi.application'

# Password validation
# https://docs.djangoproject.com/en/1.11/ref/settings/#auth-password-validators

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

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.11/howto/static-files/
STATIC_URL = '/static/'

STATICFILES_DIRS = (
                    os.path.join(BASE_DIR, "app", "static"),
                    )

STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'YOUR_NAME_HERE',
        'USER': 'YOUR_USER_HERE',
        'PASSWORD': 'YOUR_PASSWORD_HERE',
        'HOST': 'hanno.db.elephantsql.com',
        'PORT': 5432,
    }
}

USE_TZ = False

SITE_ID = 5

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
        },
    },
    'loggers': {
        'app_api': {
            'handlers': ['console'],
            'level': 'INFO',
        },
    },
    }


AUTH_PROFILE_MODULE = 'app.custom_field'
ACCOUNT_AUTHENTICATED_LOGIN_REDIRECTS = False

# ACCOUNT_FORMS = {'login': 'custom.forms.custom_login',
#                  'signup':'custom.forms.custom_signup',}
#
# SOCIALACCOUNT_FORMS = {'signup': 'custom.forms.custom_social_signup',
#                        'disconnect':'custom.forms.custom_social_disconnect',}

ACCOUNT_ADAPTER = 'app.adapter.MyAccountAdapter'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
        'rest_framework.permissions.AllowAny',
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
}

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

SOCIALACCOUNT_PROVIDERS = {
    'facebook': {
        'METHOD': 'oauth2',
        'SDK_URL': '//connect.facebook.net/{locale}/sdk.js',
        'SCOPE': ['email', 'public_profile'],
        'AUTH_PARAMS': {'auth_type': 'reauthenticate'},
        'INIT_PARAMS': {'cookie': True},
        'FIELDS': [
            'id',
            'email',
            'name',
            'first_name',
            'last_name',
            'verified',
            'locale',
            'timezone',
            'link',
            'gender',
            'updated_time',
        ],
        'EXCHANGE_TOKEN': True,
        'LOCALE_FUNC': 'path.to.callable',
        'VERIFIED_EMAIL': False,
        'VERSION': 'v7.0',
    },
    'google': {
        'SCOPE': [
            'profile',
            'email',
        ],
        'AUTH_PARAMS': {
            'access_type': 'online',
        }
    },

}

ADMINS = (
    ('Yourname', 'yourname@gmail.com'),
)

MANAGERS = ADMINS


# When you are playing around with the app and you expect that an email should
# have been sent, just run `./manage.py send_mail` and you will get the mail
# to the ADMINS account, no matter who the real recipient was.
MAILER_EMAIL_BACKEND = 'django_libs.test_email_backend.EmailBackend'
TEST_EMAIL_BACKEND_RECIPIENTS = ADMINS

FROM_EMAIL = ADMINS[0][1]
EMAIL_SUBJECT_PREFIX = '[dev IbmHack] '

EMAIL_HOST = 'smtp.gmail.com'
EMAIL_HOST_USER = FROM_EMAIL

# Enter your gmail PW from the ADMINS email entered above.
EMAIL_HOST_PASSWORD = ''
EMAIL_PORT = 587