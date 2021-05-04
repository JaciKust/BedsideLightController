import datetime

import Color as ColorConstant
import Interactable.Light.Light as LightConstant
from State.State import State


class AsleepLightsOnState(State):
    id = 2
    name = 'Asleep Lights On'

    def __init__(self, wake_time, previous_state=None, auto_alarm=True):
        if auto_alarm:
            super().__init__(previous_state)
        else:
            super().__init__(previous_state)
        self.auto_alarm = auto_alarm
        self.wake_time = wake_time
        self.all_lights_on = False

    def execute_state_change(self):
        super().execute_state_change()
        self._set_room_partial_on()

        self.plant_lights.set_off()
        self.fan.set_on()
        self.oddish_light.set_off()
        self.monitor.set_off()

    def _set_room_partial_on(self):
        LightConstant.entry_lamp.turn_on(ColorConstant.DIMMEST_WHITE, 0)
        LightConstant.jaci_bedside_lamp.turn_on(ColorConstant.DIMMEST_WHITE, 0)

    # region Button Color

    def get_primary_button_colors(self):
        if self.auto_alarm:
            return [ColorConstant.DARK_RED, ColorConstant.DIM_RED, ColorConstant.DIM_BLUE]
        return [ColorConstant.DARK_GREEN, ColorConstant.DIM_GREEN, ColorConstant.DIM_BLUE]

    def get_secondary_button_colors(self):
        return [ColorConstant.DARK_BLUE, ColorConstant.DARK_GREEN, ColorConstant.DARK_RED]

    def get_desk_rear_button_colors(self):
        return [ColorConstant.BLACK, ColorConstant.DARK_GREEN, ColorConstant.DARK_RED]

    # endregion

    # region Button Actions

    def on_primary_short_press(self):
        from State.AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(self.wake_time, self, self.auto_alarm)

    def on_primary_long_press(self):
        from State.AwakeLightsOnState import AwakeLightsOnState

        if not self.all_lights_on:
            LightConstant.all_lamp.turn_on(ColorConstant.DIMMEST_WHITE)
            self.all_lights_on = True
            return None
        else:
            return AwakeLightsOnState(self)

    def on_primary_extra_long_press(self):
        return AsleepLightsOnState(self.wake_time, self.previous_state, not self.auto_alarm)

    # endregion

    # region On Event

    def on_time_check(self):
        super().on_time_check()

        current_time = datetime.datetime.now()
        if self.auto_alarm and self.wake_time < current_time:
            from State.WakingUpState1 import WakingUpState1
            return WakingUpState1(self.wake_time)
        return None

    # endregion

    def __str__(self):
        return super().__str__() + " Alarm set: " + str(self.auto_alarm)
