import datetime
from Constants import Color as ColorConstant
from Constants import Light as LightConstant

from State.State import State


class AsleepLightsOnState(State):
    id = 2
    name = 'Asleep Lights On'

    ring_color_alarm_on = ColorConstant.DIM_RED
    ring_color_alarm_off = ColorConstant.DIM_GREEN

    on_press_ring_color_alarm_on = ColorConstant.RED
    on_press_ring_color_alarm_off = ColorConstant.GREEN

    on_long_press_ring_color = ColorConstant.BLUE

    def __init__(self, wake_time, previous_state=None, auto_alarm=True):
        if auto_alarm:
            super().__init__(self.id, self.name, self.ring_color_alarm_on, self.on_press_ring_color_alarm_on, self.on_long_press_ring_color, previous_state)
        else:
            super().__init__(self.id, self.name, self.ring_color_alarm_off, self.on_press_ring_color_alarm_off, self.on_long_press_ring_color, previous_state)
        self.auto_alarm = auto_alarm
        self.wake_time = wake_time

    def on_short_press(self):
        from State.AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(self.wake_time, self, self.auto_alarm)

    def on_long_press(self):
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_extra_long_press(self):
        return AsleepLightsOnState(self.wake_time, self.previous_state, not self.auto_alarm)

    def execute_state_change(self):
        print('changed to: ' + self.name)
        self._set_lights(LightConstant.all_group, ColorConstant.DIMMEST_WHITE, 0)

    def on_time_expire_check(self):
        current_time = datetime.datetime.now()
        if current_time > self.wake_time:
            from State.WakingUpState1 import WakingUpState1
            return WakingUpState1(self.wake_time, self)
        return None
