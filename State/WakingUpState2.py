import datetime

from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from Constants import Time as TimeConstant
from State.WakingUpState import WakingUpState


class WakingUpState2(WakingUpState):
    id = 6
    name = 'Waking Up 2'

    def __init__(self, wake_up_time):
        super().__init__(wake_up_time)
        self.state_complete_time = wake_up_time + datetime.timedelta(
            minutes=TimeConstant.waking_up_1_duration_minutes + TimeConstant.waking_up_2_duration_minutes)

    def get_primary_button_colors(self):
        return [ColorConstant.DARK_MAGENTA, ColorConstant.DARK_RED, ColorConstant.BLUE]

    def execute_state_change(self):
        self._set_lights(LightConstant.room_group, ColorConstant.WHITE,
                         TimeConstant.waking_up_2_duration_minutes * 60 * 1_000)
        self._turn_off_plant_lights()
        self._turn_on_fan()

    def on_time_expire_check(self):
        current_time = datetime.datetime.now()
        if current_time > self.state_complete_time:
            from State.AwakeLightsOnState import AwakeLightsOnState
            return AwakeLightsOnState(self)
        return None

    def __str__(self):
        return super().__str__() + "Wake Time: " + str(self.wake_up_time)
