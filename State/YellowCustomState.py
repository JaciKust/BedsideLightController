from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.CustomState import CustomState


class YellowCustomState(CustomState):
    name = 'Custom - Yellow'
    ring_color = ColorConstant.YELLOW

    def __init__(self):
        super().__init__(self.ring_color, 0, None)

    def execute_state_change(self):
        self._set_light(LightConstant.alpha, ColorConstant.WHITE, 1)
        self._set_light(LightConstant.bravo, ColorConstant.CYAN, 1)
        self._set_light(LightConstant.charlie, ColorConstant.WHITE, 1)

        self._set_light(LightConstant.delta, ColorConstant.MAGENTA, 1)
        self._set_light(LightConstant.echo, ColorConstant.CYAN, 1)
        self._set_light(LightConstant.foxtrot, ColorConstant.WHITE, 1)

        self._set_light(LightConstant.gamma, ColorConstant.MAGENTA, 1)
        self._set_light(LightConstant.hotel, ColorConstant.CYAN, 1)
        self._set_light(LightConstant.india, ColorConstant.MAGENTA, 1)

    def on_short_press(self):
        from State.CyanCustomState import CyanCustomState
        return CyanCustomState()
