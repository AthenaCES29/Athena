"""
WSGI config for Athena project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.8/howto/deployment/wsgi/
"""

import os

import django.core.handlers.wsgi

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Athena.settings")

# This application object is used by the development server
# as well as any WSGI server configured to use this file.

application = django.core.handlers.wsgi.WSGIHandler()
