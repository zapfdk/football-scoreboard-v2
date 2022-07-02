from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'^ws/controller/$', consumers.ControllerConsumer.as_asgi()),
    re_path(r'^ws/clock_controller/$', consumers.ClockControllerConsumer.as_asgi()),
]
