import ColorConstants
from State import State


class WakingUpState1(State):
    id = 6
    name = 'Waking Up 2'

    def __init__(self, previous_state=None):
        super().__init__(self, self.id, self.name, previous_state)

    def on_short_press(self):
        pass

    def on_long_press(self):
        pass

    def on_extra_long_press(self):
        pass

    def execute_state_change(self):
        pass

    def on_time_expire(self):
        pass

    def get_ring_color(self):
        return ColorConstants.CYAN

    def get_ring_color_on_press(self):
        pass
