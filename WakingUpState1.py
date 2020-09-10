import ColorConstants
from State import State


class WakingUpState1(State):
    id = 5
    name = 'Waking Up 1'
    ring_color = ColorConstants.MAGENTA
    on_press_ring_color = None
    on_long_press_ring_color = None

    def __init__(self, previous_state=None):
        super().__init__(self.id, self.name, self.ring_color, self.on_press_ring_color, self.on_long_press_ring_color, previous_state)

    def on_short_press(self):
        return self

    def on_long_press(self):
        return self

    def on_extra_long_press(self):
        return self

    def execute_state_change(self):
        print('changed to: ' + self.name)

    def on_time_expire(self):
        return self
