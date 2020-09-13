import datetime

from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.State import State


class AsleepLightsOffState(State):
    id = 1
    name = 'Asleep Lights Off'
    on_long_press_ring_color = ColorConstant.BLUE

    ring_color_alarm_on = ColorConstant.DIM_RED
    ring_color_alarm_off = ColorConstant.DIM_GREEN

    on_press_ring_color_alarm_on = ColorConstant.RED
    on_press_ring_color_alarm_off = ColorConstant.GREEN

    def __init__(self, wake_time, previous_state=None, auto_alarm=True):
        if auto_alarm:
            super().__init__(self.id, self.name, self.ring_color_alarm_on, self.on_press_ring_color_alarm_on,
                             self.on_long_press_ring_color, previous_state)
        else:
            super().__init__(self.id, self.name, self.ring_color_alarm_off, self.on_press_ring_color_alarm_off,
                             self.on_long_press_ring_color, previous_state)
        self.auto_alarm = auto_alarm
        self.wake_time = wake_time

    def on_short_press(self):
        from State.AsleepLightsOnState import AsleepLightsOnState
        return AsleepLightsOnState(self.wake_time, self, self.auto_alarm)

    def on_long_press(self):
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_extra_long_press(self):
        return AsleepLightsOffState(self.wake_time, self.previous_state, not self.auto_alarm)

    def execute_state_change(self):
        print('changed to: ' + self.name)
        from State.AwakeLightsOnState import AwakeLightsOnState

        transition_time = 0
        # If coming from Awake Lights On change over ten seconds
        if isinstance(self.previous_state, AwakeLightsOnState):
            transition_time = 10_000

        self._set_lights(LightConstant.all_group, ColorConstant.BLACK, transition_time)

    def on_time_expire_check(self):
        # Should start the wake up process
        current_time = datetime.datetime.now()
        if self.wake_time < current_time:
            from State.WakingUpState1 import WakingUpState1
            return WakingUpState1(self.wake_time, self)
        return None

    def __str__(self):
        return super().__str__() + "Alarm set: " + str(self.auto_alarm)
