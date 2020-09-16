from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.CustomState import CustomState


class YellowCustomState(CustomState):
    name = 'Custom - Yellow'
    ring_color = ColorConstant.YELLOW

    def __init__(self):
        super().__init__(self.ring_color)

    def execute_state_change(self):
        self._set_lights(LightConstant.window_group, ColorConstant.WHITE, 1)
        self._set_lights(LightConstant.room_group, ColorConstant.BLACK, 1)
