from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.CustomState import CustomState


class YellowCustomState(CustomState):
    name = 'Custom - Yellow'
    id = 7

    def __init__(self):
        super().__init__()

    def get_primary_button_colors(self):
        return [ColorConstant.YELLOW, ColorConstant.DIM_WHITE, ColorConstant.BLUE]

    def execute_state_change(self):
        super().execute_state_change()
        self._set_light(LightConstant.alpha, ColorConstant.WHITE, 1)
        # self._set_light(LightConstant.bravo, ColorConstant.CYAN, 1)
        self._set_light(LightConstant.charlie, ColorConstant.WHITE, 1)

        self._set_light(LightConstant.delta, ColorConstant.MAGENTA, 1)
        self._set_light(LightConstant.echo, ColorConstant.CYAN, 1)
        self._set_light(LightConstant.foxtrot, ColorConstant.WHITE, 1)

        self._set_light(LightConstant.golf, ColorConstant.MAGENTA, 1)
        self._set_light(LightConstant.hotel, ColorConstant.CYAN, 1)
        self._set_light(LightConstant.india, ColorConstant.MAGENTA, 1)

        self.plant_lights.set_off()
        self.fan.set_off()
        self.oddish_light.set_off()
        self.monitor.set_off()

    def on_primary_short_press(self):
        from State.CyanCustomState import CyanCustomState
        return CyanCustomState()

    def on_primary_extra_long_press(self):
        from State.Rainbow.RainbowState import RainbowState
        return RainbowState()
        pass
