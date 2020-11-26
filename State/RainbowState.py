from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from State.State import State


class RainbowState(State):
    id = 4
    name = 'Rainbow'

    def __init__(self):
        super().__init__(None)

    def get_primary_button_colors(self):
        return [ColorConstant.CYAN, ColorConstant.DARK_CYAN, ColorConstant.BLUE]

    def get_door_button_colors(self):
        return [ColorConstant.BLACK, ColorConstant.BLACK, ColorConstant.BLACK]

    def get_secondary_button_colors(self):
        return [ColorConstant.MAGENTA, ColorConstant.DARK_MAGENTA, ColorConstant.RED]

    def execute_state_change(self):
        self._set_lights(LightConstant.all_group, ColorConstant.MAGENTA, 1)
        self.plant_lights.set_off()
        self.oddish_light.set_off()

    def on_primary_short_press(self):
        # TODO: Cycle Pattern
        pass

    def on_primary_long_press(self):
        # TODO: Speed up Pattern
        pass

    def on_primary_extra_long_press(self):
        # TODO: Slow down Pattern
        pass
