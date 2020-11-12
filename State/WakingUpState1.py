import datetime

from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from Constants import Time as TimeConstant
from State.WakingUpState import WakingUpState


class WakingUpState1(WakingUpState):
    id = 5
    name = 'Waking Up 1'

    def __init__(self, wake_up_time):
        super().__init__(wake_up_time)
        self.state_complete_time = wake_up_time + datetime.timedelta(minutes=TimeConstant.waking_up_1_duration_minutes)

    def get_primary_button_colors(self):
        return [ColorConstant.DARK_CYAN, ColorConstant.DARK_RED, ColorConstant.BLUE]

    def execute_state_change(self):
        self._set_lights(LightConstant.window_group, ColorConstant.WHITE,
                         TimeConstant.waking_up_1_duration_minutes * 60 * 1_000)
        self._turn_off_plant_lights()
        self._turn_on_fan()
        self._turn_off_oddish_light()
        self._turn_off_monitor()

    def on_time_expire_check(self):
        current_time = datetime.datetime.now()
        if current_time > self.state_complete_time:
            from State.WakingUpState2 import WakingUpState2
            return WakingUpState2(self.wake_up_time)
        return None

    def __str__(self):
        return super().__str__() + "Wake Time: " + str(self.wake_up_time)
