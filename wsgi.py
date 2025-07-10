"""
WSGI config for kraken_tech_challenge_derrick_sun project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'kraken_tech_challenge_derrick_sun.settings')

application = get_wsgi_application()
