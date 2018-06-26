from django import forms
from footballscoring.definitions import Constraints

class GameClockForm(forms.Form):
    pass

class GameStateForm(forms.Form):
    down = forms.IntegerField(label='Down', min_value=1, max_value=4)
    distance = forms.IntegerField(label='Distance', min_value=-1, max_value=99)
    ball_on = forms.IntegerField(label='Ball on', min_value=1, max_value=50)
    quarter = forms.IntegerField(label='Quarter', min_value=1, max_value=4)

    


class GameConfigForm(forms.Form):
    name_home = forms.CharField(label='Name Hometeam', max_length=100)
    name_guest = forms.CharField(label='Name Guestteam', max_length=100)

