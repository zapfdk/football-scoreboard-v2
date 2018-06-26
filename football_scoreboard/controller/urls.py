from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('game_clock', views.game_clock, name='game_clock'),
    path('game_state', views.game_state, name='game_state'),
    path('game_config', views.game_config, name='game_config'),
    path('video_player', views.video_player, name='video_player'),
]