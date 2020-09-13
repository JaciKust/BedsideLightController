from Constants import Color as ColorConstant, Light, Time
import TimeFunctions
from State.State import State


class AwakeLightsOffState(State):
    id = 3
    name = 'Awake Lights Off'
    ring_color = ColorConstant.WHITE
    on_press_ring_color = ColorConstant.DIM_WHITE
    on_long_press_ring_color = ColorConstant.BLUE

    def __init__(self, previous_state=None):
        super().__init__(self.id, self.name, self.ring_color, self.on_press_ring_color, self.on_long_press_ring_color, previous_state)

    def on_short_press(self):
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_long_press(self):
        from State.AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(TimeFunctions.get_next(Time.wakeup_time), self)

    def on_extra_long_press(self):
        # Should go to Mood states
        return None

    def execute_state_change(self):
        print('changed to: ' + self.name)
        self._set_lights(Light.all_group, ColorConstant.BLACK, 1_000)

    def on_time_expire_check(self):
        # No action
        return None