from django.shortcuts import render
from django.contrib.auth.decorators import permission_required
from .web_hotkeys import hotkeys

# Create your views here.
def index(request):
    return render(request, 'controller/index.html')

@permission_required('controller.change_clock')
def game_clock(request):
    return render(request, 'controller/game_clock.html', 
    {
        "hotkeys": hotkeys["game_clock"]
    })

@permission_required('controller.change_status')
def game_state(request):
    return render(request, 'controller/game_state.html')

@permission_required('controller.change_config')
def game_config(request):
    return render(request, 'controller/game_config.html')

@permission_required('controller.play_videos')
def video_player(request):
    return render(request, 'controller/video_player.html')

