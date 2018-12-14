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
