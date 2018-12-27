from channels.generic.websocket import WebsocketConsumer
import json
from ast import literal_eval

from football_scoreboard.redis_wrapper import RedisWrapper

rw = RedisWrapper()

class ControllerConsumer(WebsocketConsumer):
    commands = {
        "SET_DOWN": "down",
        "SET_QUARTER": "quarter",
        "SET_DISTANCE": "distance",
        "SET_BALLON": "ball_on",
        "SET_SCORE": "score",
        "SET_TIMEOUTS": "timeouts",
        "SET_POSSESSION": "possession",
    }
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'msg': "UPDATE",
            "data": rw.get_current_gamestate().state
        }))

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        value = text_data_json['value']

        response = self.process_command(command, value)

        self.send(text_data=json.dumps({
            "msg": "UPDATE",
            "data": response}))

    def process_command(self, command, value):
        gs = rw.get_current_gamestate()

        if isinstance(value, str):
            val = literal_eval(value)
        else:
            val = value

        if isinstance(val, int):
            gs.set_state_property(self.commands[command], val)
        elif isinstance(val, tuple) or isinstance(val, list):
            gs.set_state_property(self.commands[command], int(val[0]), int(val[1]))

        rw.save_gamestate(gs)

        return gs.state
