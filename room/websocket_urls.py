from libs.websocket import url
from .websocket_view import connect_room, disconnect_room, send_room

urlpatterns = [
    url('/message/', connect_room, method='websocket.connect'),
    url('/message/', disconnect_room, method='websocket.disconnect'),
    url('/message/', send_room, method='websocket.receive'),
]
