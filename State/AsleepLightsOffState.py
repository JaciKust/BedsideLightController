import datetime

from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.State import State


class AsleepLightsOffState(State):
    id = 1
    name = 'Asleep Lights Off'

    def __init__(self, wake_time, previous_state=None, auto_alarm=True):
        if auto_alarm:
            super().__init__(previous_state)
        else:
            super().__init__(previous_state)
        self.auto_alarm = auto_alarm
        self.wake_time = wake_time

    def get_primary_button_colors(self):
        if self.auto_alarm:
            return [ColorConstant.DARK_RED, ColorConstant.RED, ColorConstant.BLUE]
        return [ColorConstant.DARK_GREEN, ColorConstant.GREEN, ColorConstant.BLUE]

    def on_primary_short_press(self):
        from State.AsleepLightsOnState import AsleepLightsOnState
        return AsleepLightsOnState(self.wake_time, self, self.auto_alarm)

    def on_primary_long_press(self):
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_primary_extra_long_press(self):
        return AsleepLightsOffState(self.wake_time, self.previous_state, not self.auto_alarm)

    def execute_state_change(self):
        print('changed to: ' + self.name)
        from State.AwakeLightsOnState import AwakeLightsOnState

        transition_time = 0
        # If coming from Awake Lights On change over ten seconds
        if isinstance(self.previous_state, AwakeLightsOnState):
            transition_time = 10_000

        self._set_lights(LightConstant.all_group, ColorConstant.BLACK, transition_time)
        self._turn_off_plant_lights()
        self._turn_on_fan()

    def on_time_expire_check(self):
        # Should start the wake up process
        current_time = datetime.datetime.now()
        if self.auto_alarm and self.wake_time < current_time:
            from State.WakingUpState1 import WakingUpState1
            return WakingUpState1(self.wake_time)
        return None

    def __str__(self):
        return super().__str__() + " Alarm set: " + str(self.auto_alarm)
