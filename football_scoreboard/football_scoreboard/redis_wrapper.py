import redis
import json

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

    def get_current_gameclock(self):
        if (gc := cache.get('gameclock')):
            return gc
        else:
            return 0

    def save_gameclock(self, gc):
        self.r.set('gameclock', gc.remaining_time.seconds)
