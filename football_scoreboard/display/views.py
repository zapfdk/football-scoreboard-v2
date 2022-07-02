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
    gameclock = rw.get_current_gameclock()
    gameconfig = rw.get_current_gameconfig().config

    gs = gamestate.state
    gameclock_timedelta = timedelta(seconds=gameclock)

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
            "gameclock": f"{(gameclock % 3600 // 60):02}:{(gameclock%60):02}",
            "possession": gs["possession"],
            "quarter": gs["quarter"],
            "clock_running": False,
        },
        "gameclock": gameclock,
        "gameconfig": gameconfig,
    }
    print(gamestatus)

    return JsonResponse(gamestatus)

    return JsonResponse({"gamestate": gamestate.state,
            "gameclock": gameclock,
            "gameconfig": gameconfig,
            })
