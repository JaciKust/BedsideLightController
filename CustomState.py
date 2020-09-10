import ColorConstants
from State import State


class CustomState(State):
    id = 0
    name = 'Custom'
    ring_color = ColorConstants.GREEN
    on_press_ring_color = ColorConstants.DIM_GREEN
    on_long_press_ring_color = ColorConstants.BLUE
    def __init__(self, previous_state):
        super().__init__(self.id, self.name, self.ring_color, self.on_press_ring_color, self.on_long_press_ring_color, previous_state)

    def on_short_press(self):
        from AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_long_press(self):
        from AwakeLightsOffState import AwakeLightsOffState
        return AwakeLightsOffState(self)

    def on_extra_long_press(self):
        # No planned acton
        return self

    def execute_state_change(self, lights):
        print('changed to: ' + self.name)

    def on_time_expire(self):
        return self