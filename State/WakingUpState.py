import datetime

from Constants import Time as TimeConstant
from State.State import State


class WakingUpState(State):

    def __init__(self, wake_up_time):
        self.wake_up_time = wake_up_time
        super().__init__(None)

    def on_primary_short_press(self):
        # Snooze
        new_wake_time = datetime.datetime.now() + datetime.timedelta(minutes=TimeConstant.snooze_time)
        from State.AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(new_wake_time, self)

    def on_primary_long_press(self):
        # Wake Up
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_primary_extra_long_press(self):
        # Turn off Alarm
        from State.AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(self.wake_up_time, self, False)

    def on_kelvin_changed(self):
        # Nothing should be done here.
        pass
