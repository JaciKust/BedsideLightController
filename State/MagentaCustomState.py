from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.CustomState import CustomState


class MagentaCustomState(CustomState):
    name = 'Custom - Magenta'
    ring_color = ColorConstant.DIM_MAGENTA

    def __init__(self):
        super().__init__(self.ring_color, 2, None)

    def execute_state_change(self):
        self._set_lights(LightConstant.window_group, ColorConstant.WHITE, 1)
        self._set_lights(LightConstant.room_group, ColorConstant.BLACK, 1)

    def on_short_press(self):
        from State.YellowCustomState import YellowCustomState
        return YellowCustomState()
