import ColorConstants
from State import State


class AsleepLightsOffState(State):
    id = 1
    name = 'Asleep Lights Off'

    def __init__(self, previous_state=None):
        super().__init__(self.id, self.name, previous_state)

    def on_short_press(self):
        from AsleepLightsOnState import AsleepLightsOnState
        return AsleepLightsOnState(self)

    def on_long_press(self):
        from AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_extra_long_press(self):
        # Should return itself with NO alarm set
        pass

    def execute_state_change(self):
        pass

    def on_time_expire(self):
        pass

    def get_ring_color(self):
        return ColorConstants.RED

    def get_ring_color_on_press(self):
        pass

