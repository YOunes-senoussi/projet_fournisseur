"""
ASGI config for projet_fournisseur project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from django.core.asgi import get_asgi_application
import API.web_sockets.routing

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "projet_fournisseur.settings")

application = ProtocolTypeRouter({
    'http': get_asgi_application(),
    'websocket': URLRouter(
        API.web_sockets.routing.websocket_urlpatterns
    ),
})