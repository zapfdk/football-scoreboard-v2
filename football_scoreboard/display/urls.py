from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('get_gamestatus', views.get_gamestatus, name='get_gamestatus'),
]