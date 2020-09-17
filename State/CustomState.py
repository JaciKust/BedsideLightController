from Constants import Color as ColorConstant
from State.State import State


class CustomState(State):
    id = -1
    name = 'Custom'
    on_press_ring_color = ColorConstant.DIM_WHITE
    on_long_press_ring_color = ColorConstant.BLUE
    custom_state_list = None
    current_custom_state = 0

    def __init__(self, ring_color, current_custom_state, previous_state):
        self.current_custom_state = current_custom_state
        super().__init__(self.id, self.name, ring_color, self.on_press_ring_color,
                         self.on_long_press_ring_color, previous_state)

    def on_short_press(self):
        return self.get_next_custom_state()

    def on_long_press(self):
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_extra_long_press(self):
        from State.AwakeLightsOffState import AwakeLightsOffState
        return AwakeLightsOffState(self)

    def get_next_custom_state(self):
        state_count = len(self.get_custom_state_list())
        self.current_custom_state += 1
        next_state_location = self.current_custom_state % state_count
        return self.get_custom_state_list()[next_state_location]

    def get_custom_state_list(self):
        if self.custom_state_list is not None:
            return self.custom_state_list
        from State import StateConstants
        self.custom_state_list = StateConstants.order
