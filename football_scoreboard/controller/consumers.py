from channels.generic.websocket import WebsocketConsumer
import json
from ast import literal_eval

from football_scoreboard.redis_wrapper import RedisWrapper
from footballscoring import gameclock

rw = RedisWrapper()

clock = gameclock.GameClock(quarter_length=rw.get_current_gameconfig().config["quarter_length"])

class ControllerConsumer(WebsocketConsumer):
    commands = {
        "SET_DOWN": "down",
        "SET_QUARTER": "quarter",
        "SET_DISTANCE": "distance",
        "SET_BALLON": "ball_on",
        "SET_SCORE": "score",
        "SET_TIMEOUTS": "timeouts",
        "SET_POSSESSION": "possession",
        "CHANGE_SCORE": "score",
        "CHANGE_TIMEOUTS": "timeouts",
        "SET_CONFIG_NAME": "name",
    }
    def connect(self):
        self.accept()
        self.send(text_data=json.dumps({
            'msg': "UPDATE",
            "gamestate": rw.get_current_gamestate().state,
            "gameconfig": rw.get_current_gameconfig().config
        }))

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        value = text_data_json['value']

        status = "successful"

        try:
            response = self.process_command(command, value)
        except Exception as e:
            print(str(e))
            status = "not sucessfull"
            response = rw.get_current_gamestate().state

        self.send(text_data=json.dumps({
            "msg": "UPDATE",
            "gamestate": rw.get_current_gamestate().state,
            "gameconfig": rw.get_current_gameconfig().config,
            "transmittedCommand": "{}, {}".format(command, value),
            "transmissionStatus": status,
            }
        ))

    def process_command(self, command, value):
        if isinstance(value, str):
            val = literal_eval(value)
        else:
            val = value

        if "CONFIG" in command:
            gc = rw.get_current_gameconfig()
            print(gc.config)
            if "NAME" in command:
                if isinstance(val, int):
                    pass
                elif isinstance(val, tuple) or isinstance(val, list):
                    print(value)

                    gc.config["name"][val[1]] = val[0]
                    print(gc.config)

            rw.save_gameconfig(gc)

        else:
            gs = rw.get_current_gamestate()
            if "SET" in command:
                if isinstance(val, int):
                    gs.set_state_property(self.commands[command], val)
                elif isinstance(val, tuple) or isinstance(val, list):
                    gs.set_state_property(self.commands[command], int(val[0]), int(val[1]))
            elif "CHANGE" in command:
                if isinstance(val, int):
                    gs.modify_state_property(self.commands[command], val)
                elif isinstance(val, tuple) or isinstance(val, list):
                    gs.modify_state_property(self.commands[command], int(val[0]), int(val[1]))

            rw.save_gamestate(gs)


class ClockControllerConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        clock.callback = self.clock_callback

        self.send(text_data=json.dumps({
            'msg': "UPDATE",
        }))

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        print(text_data_json)
        command = text_data_json['command']
        value = text_data_json['value']

        if command == "TOGGLE_CLOCK":
            clock.toggle()
        elif command == "RESET_QUARTER":
            clock.reset_clock()
        elif command == "SET_CLOCK":
            minutes, seconds = value.split(":")
            minutes, seconds = int(minutes), int(seconds)
            clock.set_clock(minutes=minutes, seconds=seconds)

    def clock_callback(self):
        self.send(text_data=json.dumps({
            "time": clock.remaining_time.seconds,
            "running": clock.running,
        }))
