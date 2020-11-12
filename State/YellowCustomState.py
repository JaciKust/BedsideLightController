from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.CustomState import CustomState


class YellowCustomState(CustomState):
    name = 'Custom - Yellow'

    def __init__(self):
        super().__init__()

    def get_primary_button_colors(self):
        return [ColorConstant.YELLOW, ColorConstant.DIM_WHITE, ColorConstant.BLUE]

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

        self._turn_off_plant_lights()
        self._turn_off_fan()
        self._turn_off_oddish_light()

    def on_primary_short_press(self):
        from State.CyanCustomState import CyanCustomState
        return CyanCustomState()
