from channels.generic.websocket import WebsocketConsumer
import json
from ast import literal_eval
from datetime import timedelta

from football_scoreboard.redis_wrapper import RedisWrapper
from footballscoring import gameclock

rw = RedisWrapper()

_clock_consumers = set()
_last_broadcast_second = None
_clock_scheduler_started = False
_clock_loop_callback = None


def _ensure_game_clock_callbacks():
    if getattr(gameclock.GameClock, '_scoreboard_callbacks_patched', False):
        return

    original_process_clock = gameclock.GameClock.process_clock

    def process_clock(self):
        global _clock_loop_callback
        was_running = self.running
        original_process_clock(self)
        if was_running and _clock_loop_callback:
            _clock_loop_callback()

    def set_loop_callback(self, callback):
        global _clock_loop_callback
        _clock_loop_callback = callback

    gameclock.GameClock.process_clock = process_clock
    gameclock.GameClock.set_loop_callback = set_loop_callback
    gameclock.GameClock._scoreboard_callbacks_patched = True


def _restore_clock_from_microseconds(clock_obj, microseconds):
    clock_obj.remaining_time = timedelta(microseconds=int(microseconds))
    clock_obj.running = False


_ensure_game_clock_callbacks()


def _ensure_clock_scheduler():
    global _clock_scheduler_started
    if _clock_scheduler_started:
        return
    clock.start()
    clock.running = False
    _clock_scheduler_started = True


def _clock_payload():
    return {
        "time": int(clock.remaining_time.total_seconds()),
        "running": clock.running,
    }


def _invalidate_broadcast_throttle():
    global _last_broadcast_second
    _last_broadcast_second = None


def _broadcast_clock_state(force=False):
    global _last_broadcast_second
    current_second = int(clock.remaining_time.total_seconds())
    if not force and _last_broadcast_second == current_second:
        return
    _last_broadcast_second = current_second
    payload = json.dumps(_clock_payload())
    dead = set()
    global _clock_consumers
    for consumer in _clock_consumers:
        try:
            consumer.send(text_data=payload)
        except Exception:
            dead.add(consumer)
    _clock_consumers -= dead


def _on_clock_tick():
    rw.save_gameclock_microseconds(clock)
    if _clock_consumers:
        _broadcast_clock_state()


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
            self.process_command(command, value)
        except Exception as e:
            print(str(e))
            status = "not sucessfull"

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
clock = gameclock.GameClock(
    quarter_length=rw.get_current_gameconfig().config["quarter_length"],
    interval_ms=100,
)
if current_gameclock_microseconds is not None:
    _restore_clock_from_microseconds(clock, current_gameclock_microseconds)

rw.save_gameclock_microseconds(clock)


class ClockControllerConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()
        _ensure_clock_scheduler()
        _clock_consumers.add(self)
        clock.set_loop_callback(_on_clock_tick)
        _invalidate_broadcast_throttle()
        _broadcast_clock_state(force=True)

    def disconnect(self, code):
        _clock_consumers.discard(self)
        if not _clock_consumers:
            clock.set_loop_callback(None)

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
            clock.set_clock(minutes=minutes, seconds=seconds)
        rw.save_gameclock_microseconds(clock)
        _invalidate_broadcast_throttle()
        _broadcast_clock_state(force=True)
