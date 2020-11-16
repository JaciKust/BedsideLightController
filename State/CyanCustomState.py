from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.CustomState import CustomState


class CyanCustomState(CustomState):
    name = 'Custom - Cyan'
    id = 5

    def __init__(self):
        super().__init__()

    def get_primary_button_colors(self):
        return [ColorConstant.CYAN, ColorConstant.DIM_WHITE, ColorConstant.BLUE]

    def execute_state_change(self):
        super().execute_state_change()
        self._set_lights(LightConstant.window_group, ColorConstant.WHITE, 1)
        self._set_lights(LightConstant.room_group, ColorConstant.BLACK, 1)
        self._set_lights(LightConstant.india, ColorConstant.WHITE, 1)

        self.plant_lights.set_off()
        self.fan.set_off()
        self.oddish_light.set_on()
        self.monitor.set_on()

    def on_primary_short_press(self):
        from State.MagentaCustomState import MagentaCustomState
        return MagentaCustomState()
