"""
Defines hotkeys for the web interfaces. 
First level defines the page, second level defines the action as key, 
and the tuple of the human readable keyname and the Javascript key code.
"""
hotkeys = {
    "game_clock": {
        "toggle_clock": ("Space", 32),
        "reset_quarter": ("Q", 81),
    },
    "game_state": {
        "select_down": ("D", 68),
        "select_quarter": ("Q", 81),
        "select_distance": ("T", 84),
        "select_ballon": ("B", 66),
    },
}