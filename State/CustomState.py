from Constants import Color as ColorConstant
from State.State import State


class CustomState(State):
    id = 0
    name = 'Custom'
    ring_color = ColorConstant.GREEN
    on_press_ring_color = ColorConstant.DIM_GREEN
    on_long_press_ring_color = ColorConstant.BLUE

    def __init__(self, previous_state):
        super().__init__(self.id, self.name, self.ring_color, self.on_press_ring_color, self.on_long_press_ring_color, previous_state)

    def on_short_press(self):
        # Should rotate through custom settings here
        return None

    def on_long_press(self):
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_extra_long_press(self):
        from State.AwakeLightsOffState import AwakeLightsOffState
        return AwakeLightsOffState(self)

    def execute_state_change(self):
        print('changed to: ' + self.name)

    def on_time_expire_check(self):
        # No action
        return None
