"""
WSGI config for autorent project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""
import os
import django
from django.utils.encoding import force_str
from django.core.wsgi import get_wsgi_application


django.utils.encoding.force_text = force_str

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "autorent.settings_prod")

application = get_wsgi_application()
