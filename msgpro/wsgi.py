"""
WSGI config for msgpro project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.9/howto/deployment/wsgi/
"""

import os

import newrelic.agent
newrelic.agent.initialize('/home/diogo/webapps/msgpro/msgpro/newrelic.ini')

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "msgpro.settings")

application = get_wsgi_application()
application = newrelic.agent.wsgi_application()(application)
