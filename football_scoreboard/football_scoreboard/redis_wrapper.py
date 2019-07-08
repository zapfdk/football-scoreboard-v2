import redis
import json

from footballscoring import gamestate, gameclock, gameconfig

HOST = 'localhost'
PORT = 6379
DB = 0


class RedisWrapper:
    def __init__(self):
        self.r = redis.StrictRedis(host=HOST, port=PORT, db=DB)

    def get_current_gamestate(self):
        if not self.r.get('gamestate'):
            return gamestate.GameState()
        else:
            return self._get_gamestate_from_redis()

    def _get_gamestate_from_redis(self):
        return gamestate.GameState(json.loads(self.r.get('gamestate')))

    def save_gamestate(self, gamestate):
        self.r.set('gamestate', json.dumps(gamestate.state))

    def get_current_gameconfig(self):
        if not self.r.get('gameconfig'):
            return gamestate.GameConfig()
        else:
            return self._get_gameconfig_from_redis()

    def _get_gameconfig_from_redis(self):
        return gamestate.GameConfig(json.loads(self.r.get('gameconfig')))

    def save_gameconfig(self, gameconfig):
        self.r.set('gameconfig', json.dumps(gameconfig.config))

    def get_current_gameclock(self):
        if not self.r.get('gameclock'):
            return 0
        else:
            return self._get_gameclock_from_redis()
    def _get_gameclock_from_redis(self):
        return int(self.r.get('gameclock'))

    def save_gameclock(self, gameclock):
        self.r.set('gameclock', gameclock.remaining_time.seconds)