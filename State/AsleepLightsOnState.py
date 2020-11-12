import datetime

from Constants import Color as ColorConstant
from Constants import Light as LightConstant
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

    def get_primary_button_colors(self):
        if self.auto_alarm:
            return [ColorConstant.DARK_RED, ColorConstant.RED, ColorConstant.BLUE]
        return [ColorConstant.DARK_GREEN, ColorConstant.GREEN, ColorConstant.BLUE]

    def get_secondary_button_colors(self):
        return [ColorConstant.DARK_BLUE, ColorConstant.DARK_GREEN, ColorConstant.DARK_RED]

    def on_primary_short_press(self):
        from State.AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(self.wake_time, self, self.auto_alarm)

    def on_primary_long_press(self):
        from State.AwakeLightsOnState import AwakeLightsOnState

        if not self.all_lights_on:
            self._set_room_all_on()
            self.all_lights_on = True
            return None
        else:
            return AwakeLightsOnState(self)

    def on_primary_extra_long_press(self):
        return AsleepLightsOnState(self.wake_time, self.previous_state, not self.auto_alarm)

    def execute_state_change(self):
        print('changed to: ' + self.name)
        self._set_room_partial_on()
        self._turn_off_plant_lights()
        self._turn_on_fan()
        self._turn_off_oddish_light()

    def on_time_expire_check(self):
        current_time = datetime.datetime.now()
        if self.auto_alarm and self.wake_time < current_time:
            from State.WakingUpState1 import WakingUpState1
            return WakingUpState1(self.wake_time)
        return None

    def _set_room_partial_on(self):
        self._set_light(LightConstant.india, ColorConstant.DIMMEST_WHITE, 0)
        self._set_lights(LightConstant.window_group, ColorConstant.DIMMEST_WHITE, 0)

    def _set_room_all_on(self):
        self._set_lights(LightConstant.all_group, ColorConstant.DIMMEST_WHITE, 0)

    def __str__(self):
        return super().__str__() + " Alarm set: " + str(self.auto_alarm)
