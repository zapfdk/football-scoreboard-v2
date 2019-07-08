from django.shortcuts import render
from django.http import JsonResponse

from football_scoreboard.redis_wrapper import RedisWrapper

rw = RedisWrapper()

# Create your views here.
def index(request):
    return render(request, 'display/display.html')

def get_gamestatus(request):
    gamestate = rw.get_current_gamestate().state
    gameclock = rw.get_current_gameclock()
    gameconfig = rw.get_current_gameconfig().config

    return JsonResponse({"gamestate": gamestate,
            "gameclock": gameclock,
            "gameconfig": gameconfig,
            })
