"""
Django settings for {{ project_name }} project.

For more information on this file, see
https://docs.djangoproject.com/en/{{ docs_version }}/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/{{ docs_version }}/ref/settings/
"""
import os
import yaml

from configurations import Configuration, values


def load_logging_config(path):
    """
    Loads the logging configuration from a yaml file and returns the configuration as a dictionary
    :return :logging configuration dictionary
    """
    if os.path.exists(path):
        try:
            with open(path, 'rt') as f:
                return yaml.safe_load(f.read())
        except (IOError, ValueError) as e:
            print("Error loading logging configuration.")
            print(e)
        return {}


class Common(Configuration):
    PROJECT_NAME = "{{ project_name }}"

    # Build paths inside the project like this: os.path.join(BASE_DIR, ...)
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # This is the directory under which all the assets will be stored
    ASSETS_DIR = os.path.join(BASE_DIR, 'assets')

    # Directory for uploaded media files and collected static files
    CONTENTS_DIR = os.path.join(BASE_DIR, 'contents')

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/2.1/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = values.SecretValue()

    DEBUG = values.BooleanValue(False)

    ALLOWED_HOSTS = values.ListValue([])


    # Application definition
    INSTALLED_APPS = [
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'django.contrib.sites',

        # extends core functionality
        'rest_framework',
        'django_extensions',
        'widget_tweaks',
        'extra_views',

        # 3rd party
        'allauth',
        'allauth.account',
        'allauth.socialaccount',
        'allauth.socialaccount.providers.openid',
        'allauth.socialaccount.providers.google',
        'avatar',
        'passwords',
        'gdpr_assist',
        'bootstrap4',
        'fontawesome',

        # local
        'theme',
        'custom_auth',
    ]

    MIDDLEWARE = [
        'django.middleware.security.SecurityMiddleware',
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',

        '{{ project_name }}.middleware.TimezoneMiddleware',
    ]

    ROOT_URLCONF = '{{ project_name }}.urls'

    TEMPLATES = [
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'DIRS': [os.path.join(ASSETS_DIR, 'templates')],
            'APP_DIRS': True,
            'OPTIONS': {
                'context_processors': [
                    'django.template.context_processors.debug',
                    'django.template.context_processors.request',
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',

                    '{{ project_name }}.context_processors.project',
                    'theme.context_processors.theme',
                ],
            },
        },
    ]

    WSGI_APPLICATION = '{{ project_name }}.wsgi.application'

    APPEND_SLASH = values.BooleanValue(True)

    # Database
    # https://docs.djangoproject.com/en/2.1/ref/settings/#databases

    DATABASES  = {
        'gdpr_log': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': os.path.join(BASE_DIR, 'gdpr-log.sqlite3'),
        },
    }
    DATABASE_ROUTERS = ['gdpr_assist.routers.EventLogRouter']


    # Password validation
    # https://docs.djangoproject.com/en/2.1/ref/settings/#auth-password-validators
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

    AUTH_USER_MODEL = 'custom_auth.User'
    # Internationalization
    # https://docs.djangoproject.com/en/2.1/topics/i18n/

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    AUTHENTICATION_BACKENDS = (
        # Needed to login by username in Django admin, regardless of `allauth`
        "django.contrib.auth.backends.ModelBackend",
        # `allauth` specific authentication methods, such as login by e-mail
        "allauth.account.auth_backends.AuthenticationBackend",
    )

    SITE_ID = 1

    ACCOUNT_AUTHENTICATION_METHOD = 'username_email'
    ACCOUNT_USER_MODEL_USERNAME_FIELD = 'username'
    ACCOUNT_EMAIL_REQUIRED = True
    ACCOUNT_USERNAME_REQUIRED = False
    ACCOUNT_SIGNUP_PASSWORD_ENTER_TWICE = True
    ACCOUNT_SESSION_REMEMBER = True
    ACCOUNT_UNIQUE_EMAIL = True

    ACCOUNT_FORMS = {
        'change_password': 'custom_auth.forms.ChangePasswordForm'
    }

    LOGIN_URL = 'account_login'
    LOGOUT_URL = 'account_logout'
    LOGIN_REDIRECT_URL = 'index'
    ACCOUNT_LOGOUT_REDIRECT_URL = 'index'

    AVATAR_EXPOSE_USERNAMES = False

    PASSWORD_COMPLEXITY = {
        "UPPER": 1,   # Uppercase
        "LOWER": 1,   # Lowercase
        "LETTERS": 1, # Either uppercase or lowercase letters
        "DIGITS": 1,  # Digits
    }

    LANGUAGE_CODE = values.Value('en-us')

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    LOGGING = load_logging_config('logging.yaml')

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/2.1/howto/static-files/

    MEDIA_URL = values.Value('/media/')

    STATIC_URL = values.Value('/statics/')

    MEDIA_ROOT = os.path.join(CONTENTS_DIR, 'media')

    STATIC_ROOT = os.path.join(CONTENTS_DIR, 'statics')

    STATICFILES_DIRS = (
        os.path.join(ASSETS_DIR, 'static'),
    )

    LOCALE_PATHS = (
        os.path.join(ASSETS_DIR, 'locale'),
    )

    FIXTURE_DIRS = (
        os.path.join(ASSETS_DIR, 'fixtures'),
    )

    THEME_ROOT = 'theme/'


class Development(Common):
    """
    The in-development settings and the default configuration.
    """
    DEBUG = values.BooleanValue(True)

    ALLOWED_HOSTS = values.ListValue([])

    INTERNAL_IPS = values.ListValue([])

    INSTALLED_APPS = Common.INSTALLED_APPS + [
        'debug_toolbar',
    ]

    MIDDLEWARE = Common.MIDDLEWARE + [
        'debug_toolbar.middleware.DebugToolbarMiddleware'
    ]

    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    DATABASES = Common.DATABASES
    DATABASES = values.DatabaseURLValue(
        'sqlite:///{}'.format(os.path.join(Common.BASE_DIR, 'db.sqlite3'))
    )


class Staging(Common):
    """
    The in-staging settings.
    """
    # Security
    SESSION_COOKIE_SECURE = values.BooleanValue(True)
    SECURE_BROWSER_XSS_FILTER = values.BooleanValue(True)
    SECURE_CONTENT_TYPE_NOSNIFF = values.BooleanValue(True)
    SECURE_HSTS_INCLUDE_SUBDOMAINS = values.BooleanValue(True)
    SECURE_HSTS_SECONDS = values.IntegerValue(31536000)
    SECURE_REDIRECT_EXEMPT = values.ListValue([])
    SECURE_SSL_HOST = values.Value(None)
    SECURE_SSL_REDIRECT = values.BooleanValue(True)
    SECURE_PROXY_SSL_HEADER = values.TupleValue(
        ('HTTP_X_FORWARDED_PROTO', 'https')
    )

    DATABASES = Common.DATABASES
    DATABASES = values.DatabaseURLValue(
        'postgres://projuser:projword@localhost/default'
    )


class Production(Staging):
    """
    The in-production settings.
    """
    pass

