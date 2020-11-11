from Constants import Color as ColorConstant
from State.State import State


class CustomState(State):
    id = -1
    name = 'Custom'

    custom_state_list = None
    current_custom_state = 0

    def __init__(self):
        super().__init__(None)

    def get_door_button_colors(self):
        return [ColorConstant.WHITE, ColorConstant.DIM_WHITE, ColorConstant.BLACK]

    def on_primary_long_press(self):
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_primary_extra_long_press(self):
        from State.AwakeLightsOffState import AwakeLightsOffState
        return AwakeLightsOffState(self)

    def on_door_short_press(self):
        return self.on_primary_long_press()

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
