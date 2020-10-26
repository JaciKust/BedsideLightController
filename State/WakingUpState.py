import datetime

from Constants import Color as ColorConstant
from Constants import Time as TimeConstant
from State.State import State


class WakingUpState(State):
    on_press_ring_color = ColorConstant.DARK_RED
    on_long_press_ring_color = ColorConstant.BLUE

    def __init__(self, id, name, ring_color, wake_up_time):
        self.wake_up_time = wake_up_time
        super().__init__(id, name, ring_color, self.on_press_ring_color, self.on_long_press_ring_color, None)

    def on_short_press(self):
        # Snooze
        new_wake_time = datetime.datetime.now() + datetime.timedelta(minutes=TimeConstant.snooze_time)
        from State.AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(new_wake_time, self)

    def on_long_press(self):
        # Wake Up
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_extra_long_press(self):
        # Turn off Alarm
        from State.AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(self.wake_up_time, self, False)
