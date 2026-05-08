import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'jatte.settings')


from django.core.asgi import get_asgi_application
django_asgi_application = get_asgi_application()

from channels.auth import AuthMiddlewareStack
from channels.routing import URLRouter,ProtocolTypeRouter
from channels.security.websocket import AllowedHostsOriginValidator
from chat import routing

application=ProtocolTypeRouter({
    'http':django_asgi_application,
    'websocket':AllowedHostsOriginValidator(AuthMiddlewareStack(URLRouter(routing.websocket_urlpatterns)))
})