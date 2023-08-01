"""."""

from pathlib import Path

import dj_database_url
from django.conf import settings
from dotenv import read_dotenv


def pytest_configure() -> None:
    read_dotenv(str(Path(__file__).parent.parent / '.env'))
    settings_params = {
        'SECRET_KEY': 'abcd',
        'INSTALLED_APPS': [
            # Mandatory
            'django.contrib.contenttypes',
            # Permissions
            'django.contrib.auth',
            # Admin
            'django.contrib.admin',
            'django.contrib.messages',
            'django.contrib.sessions',
            # Project
            'rest_framework',
            'rest_framework_api_key',
            'test_project.heroes',
        ],
        'TEMPLATES': [
            # Admin
            {
                'BACKEND': 'django.template.backends.django.DjangoTemplates',
                'OPTIONS': {
                    'context_processors': [
                        'django.contrib.auth.context_processors.auth',
                        'django.contrib.messages.context_processors.messages',
                    ]
                },
            }
        ],
        'MIDDLEWARE': [
            # Admin
            'django.contrib.sessions.middleware.SessionMiddleware',
            'django.contrib.messages.middleware.MessageMiddleware',
            'django.contrib.auth.middleware.AuthenticationMiddleware',
        ],
        'ROOT_URLCONF': 'test_project.project.urls',
        'DATABASES': {
            'default': dj_database_url.config(default='sqlite://:memory:'),
            'test': dj_database_url.config(default='sqlite://:memory:'),
        },
    }
    settings.configure(**settings_params)
