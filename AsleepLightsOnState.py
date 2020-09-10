import ColorConstants
from State import State


class AsleepLightsOnState(State):
    id = 2
    name = 'Asleep Lights On'

    def __init__(self, previous_state=None):
        super().__init__(self.id, self.name, previous_state)

    def on_short_press(self):
        from AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(self)

    def on_long_press(self):
        from AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_extra_long_press(self):
        # No planned action
        pass

    def execute_state_change(self):
        pass

    def on_time_expire(self):
        pass

    def get_ring_color(self):
        return ColorConstants.BLUE

    def get_ring_color_on_press(self):
        pass
