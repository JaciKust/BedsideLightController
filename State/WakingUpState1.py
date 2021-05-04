import datetime

import Color as ColorConstant
import Interactable.Light.Light as LightConstant
from Constants import Time as TimeConstant
from State.WakingUpState import WakingUpState


class WakingUpState1(WakingUpState):
    id = 8
    name = 'Waking Up 1'

    def __init__(self, wake_up_time):
        super().__init__(wake_up_time)
        self.state_complete_time = wake_up_time + datetime.timedelta(minutes=TimeConstant.waking_up_1_duration_minutes)

    def execute_state_change(self):
        super().execute_state_change()
        transition_time = TimeConstant.waking_up_1_duration_minutes * 60 * 1_000
        LightConstant.desk_lamp.turn_on(self.current_white, transition_time)

        self.plant_lights.set_off()
        self.fan.set_on()
        self.oddish_light.set_off()
        self.monitor.set_off()

    # region Button Color

    def get_primary_button_colors(self):
        return [ColorConstant.DARK_CYAN, ColorConstant.DARK_RED, ColorConstant.BLUE]

    # endregion

    # region On Event

    def on_time_check(self):
        super().on_time_check()

        current_time = datetime.datetime.now()
        if current_time > self.state_complete_time:
            from State.WakingUpState2 import WakingUpState2
            return WakingUpState2(self.wake_up_time)
        return None

    # endregion

    def __str__(self):
        return super().__str__() + "Wake Time: " + str(self.wake_up_time)
