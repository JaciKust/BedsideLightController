from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.CustomState import CustomState


class CyanCustomState(CustomState):
    name = 'Custom - Cyan'

    def __init__(self):
        super().__init__()

    def get_primary_button_colors(self):
        return [ColorConstant.CYAN, ColorConstant.DIM_WHITE, ColorConstant.BLUE]

    def execute_state_change(self):
        self._set_lights(LightConstant.window_group, ColorConstant.WHITE, 1)
        self._set_lights(LightConstant.room_group, ColorConstant.BLACK, 1)
        self._set_lights(LightConstant.india, ColorConstant.WHITE, 1)
        self._turn_off_plant_lights()
        self._turn_off_fan()
        self._turn_on_oddish_light()
        self._turn_on_monitor()

    def on_primary_short_press(self):
        from State.MagentaCustomState import MagentaCustomState
        return MagentaCustomState()
