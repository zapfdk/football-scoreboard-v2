import redis
import json
from datetime import timedelta as td

from django.core.cache import cache

from footballscoring import gamestate, gameclock, gameconfig

HOST = 'localhost'
PORT = 6379
DB = 0


class RedisWrapper:
    def __init__(self):
        self.r = redis.StrictRedis(host=HOST, port=PORT, db=DB)

    def get_current_gamestate(self):
        if (gs := cache.get('gamestate')):
            return gs
        else:
            return gamestate.GameState()

    def save_gamestate(self, gs):
        cache.set('gamestate', gs)

    def get_current_gameconfig(self):
        if (gc := cache.get('gameconfig')):
            return gc
        else:
            return gamestate.GameConfig(quarter_length=12)

    def save_gameconfig(self, gc):
        cache.set('gameconfig', gc)

    def get_current_gameclock_microseconds(self):
        gc = cache.get('gameclock')
        if gc is not None:
            return gc
        else:
            return None 

    def save_gameclock_microseconds(self, gc):
        cache.set('gameclock', gc.remaining_time / td(microseconds=1))
