"""
WSGI config for tcr_tracker project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/2.2/howto/deployment/wsgi/
"""

import os

import sentry_sdk
from django.conf import settings
from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'tcr_tracker.settings')

application = get_wsgi_application()
if settings.SENTRY_API_KEY:
    sentry_sdk.init(settings.SENTRY_API_KEY)
