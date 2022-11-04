"""
ASGI config for backend project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.0/howto/deployment/asgi/
"""

import os
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack
from django.core.asgi import get_asgi_application
from chat.consumers import PrivateChatConsumer
from django.urls import path

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')

application = get_asgi_application()

application = ProtocolTypeRouter({
	"websocket": AuthMiddlewareStack(
		URLRouter([
			path('ws/<int:id>/', PrivateChatConsumer.as_asgi())
		])
	)
})
