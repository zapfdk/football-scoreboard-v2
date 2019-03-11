from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^ws/controller/$', consumers.ControllerConsumer),
    url(r'^ws/clock_controller/$', consumers.ClockControllerConsumer),
]