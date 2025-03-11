from channels.generic.websocket import WebsocketConsumer
import json
from ast import literal_eval

from football_scoreboard.redis_wrapper import RedisWrapper
from footballscoring import gameclock

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
        "CHANGE_SCORE": "score",
        "CHANGE_TIMEOUTS": "timeouts",
        "SET_CONFIG_NAME": "name",
        "TOGGLE_CLOCK": ""
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

current_gameclock_microseconds = rw.get_current_gameclock_microseconds()
clock = gameclock.GameClock(quarter_length=rw.get_current_gameconfig().config["quarter_length"])
clock.start()
clock.stop()
if current_gameclock_microseconds is not None:
    clock.set_clock(minutes=0, seconds=0, microseconds=current_gameclock_microseconds)

rw.save_gameclock_microseconds(clock)

class ClockControllerConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        clock.set_loop_callback(self.clock_callback)

        self.send(text_data=json.dumps({
            'msg': "UPDATE",
            "time": clock.remaining_time.seconds,
            "running": clock.running,
        }))

    def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        command = text_data_json['command']
        value = text_data_json['value']

        if command == "TOGGLE_CLOCK":
            clock.toggle()
        elif command == "RESET_QUARTER":
            clock.reset_clock()
        elif command == "SET_CLOCK":
            hours, minutes, seconds = value.split(":")
            minutes, seconds = int(minutes), int(seconds)
            clock.set_clock(minutes=minutes, seconds=seconds, microseconds=0)
        rw.save_gameclock_microseconds(clock)
        self.send(text_data=json.dumps({
            "time": clock.remaining_time.seconds,
            "running": clock.running,
        }))

    def clock_callback(self):
        rw.save_gameclock_microseconds(clock)

        self.send(text_data=json.dumps({
            "time": clock.remaining_time.seconds,
            "running": clock.running,
        }))
