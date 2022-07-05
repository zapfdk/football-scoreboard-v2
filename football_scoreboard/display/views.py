from datetime import timedelta

from django.shortcuts import render
from django.http import JsonResponse

from football_scoreboard.redis_wrapper import RedisWrapper

rw = RedisWrapper()

# Create your views here.
def index(request):
    return render(request, 'display/display.html')

def convert_gamestate(gamestate):
    return {
        ""

    }

def get_gamestatus(request):
    gamestate = rw.get_current_gamestate()
    gameclock = rw.get_current_gameclock_microseconds()
    gameconfig = rw.get_current_gameconfig().config
    gameclock_seconds = gameclock // 1e6

    gs = gamestate.state

    gamestatus = {
        "gamestate": {
            "down": gs["down"],
            "distance": gs["distance"],
            "ball_on": gs["ball_on"],
            "score_home": gs["score"][0],
            "score_guest": gs["score"][1],
            "name_home": gameconfig["name"][0],
            "name_guest": gameconfig["name"][1],
            "timeouts_home": gs["timeouts"][0],
            "timeouts_guest": gs["timeouts"][1],
            "gameclock": f"{(gameclock_seconds % 3600 // 60):02}:{(gameclock_seconds%60):02}",
            "possession": gs["possession"],
            "quarter": gs["quarter"],
            "clock_running": False,
        },
        "gameclock": gameclock_seconds,
        "gameconfig": gameconfig,
    }

    return JsonResponse(gamestatus)
