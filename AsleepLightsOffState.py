import ColorConstants
from State import State


class AsleepLightsOffState(State):
    id = 1
    name = 'Asleep Lights Off'
    ring_color = ColorConstants.DIM_RED
    on_press_ring_color = ColorConstants.RED
    on_long_press_ring_color = ColorConstants.BLUE

    def __init__(self, previous_state=None):
        super().__init__(self.id, self.name, self.ring_color, self.on_press_ring_color, self.on_long_press_ring_color, previous_state)

    def on_short_press(self):
        from AsleepLightsOnState import AsleepLightsOnState
        return AsleepLightsOnState(self)

    def on_long_press(self):
        from AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_extra_long_press(self):
        # Should return itself with NO alarm set
        return self

    def execute_state_change(self):
        print('changed to: ' + self.name)

    def on_time_expire(self):
        return self
