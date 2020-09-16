from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.CustomState import CustomState


class CyanCustomState(CustomState):
    name = 'Custom - Cyan'
    ring_color = ColorConstant.YELLOW

    def __init__(self, previous_state):
        super().__init__(self.ring_color)

    def execute_state_change(self):
        self._set_lights(LightConstant.window_group, ColorConstant.WHITE, 1)
        self._set_lights(LightConstant.room_group, [16, 16, 16], 1)
