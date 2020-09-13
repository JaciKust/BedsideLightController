import datetime
from Constants import Color as ColorConstant
from Constants import Time as TimeConstant
from Constants import Light as LightConstant
from State.State import State


class WakingUpState2(State):
    id = 6
    name = 'Waking Up 2'
    ring_color = ColorConstant.CYAN
    on_press_ring_color = ColorConstant.DIM_RED
    on_long_press_ring_color = ColorConstant.BLUE

    def __init__(self, wake_up_time, previous_state=None):
        super().__init__(self.id, self.name, self.ring_color, self.on_press_ring_color, self.on_long_press_ring_color, previous_state)
        self.wake_up_time = wake_up_time
        self.state_complete_time = wake_up_time + datetime.timedelta(minutes=TimeConstant.waking_up_1_duration_minutes + TimeConstant.waking_up_2_duration_minutes)

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

    def execute_state_change(self):
        self._set_lights(LightConstant.room_group, ColorConstant.WHITE,
                         TimeConstant.waking_up_2_duration_minutes * 60 * 1_000)

    def on_time_expire_check(self):
        current_time = datetime.datetime.now()
        if current_time > self.state_complete_time:
            from State.AwakeLightsOnState import AwakeLightsOnState
            return AwakeLightsOnState(self)
        return None
