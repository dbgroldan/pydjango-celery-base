from channels.auth  import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
import reports.routing

application = ProtocolTypeRouter({
    'websocket': AuthMiddlewareStack(
        URLRouter(
            reports.routing.websocket_urlpatterns
        )
    )
})

