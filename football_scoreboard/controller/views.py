from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'controller/index.html')

def game_clock(request):
    return render(request, 'controller/game_clock.html')

def game_state(request):
    return render(request, 'controller/game_state.html')

def game_config(request):
    return render(request, 'controller/game_config.html')

def video_player(request):
    return render(request, 'controller/video_player.html')

