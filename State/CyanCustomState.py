from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.CustomState import CustomState


class CyanCustomState(CustomState):
    name = 'Custom - Cyan'
    ring_color = ColorConstant.CYAN

    def __init__(self):
        super().__init__(self.ring_color, 1, None)

    def execute_state_change(self):
        self._set_lights(LightConstant.window_group, ColorConstant.WHITE, 1)
        self._set_lights(LightConstant.room_group, ColorConstant.BLACK, 1)
        self._set_lights(LightConstant.india, ColorConstant.WHITE, 1)

    def on_short_press(self):
        from State.MagentaCustomState import MagentaCustomState
        return MagentaCustomState()
