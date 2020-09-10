import AwakeLightsOffState
import ColorConstants
from State import State


class AwakeLightsOnState(State):
    id = 4
    name = 'Awake Lights On'

    def __init__(self, previous_state=None):
        super().__init__(self, self.id, self.name, previous_state)

    def on_short_press(self):
        var = AwakeLightsOffState(self)
        return var

    def on_long_press(self):
        pass

    def on_extra_long_press(self):
        pass

    def execute_state_change(self):
        pass

    def on_time_expire(self):
        pass

    def get_ring_color(self):
        return ColorConstants.YELLOW

    def get_ring_color_on_press(self):
        pass
