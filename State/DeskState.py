import threading

import Color as ColorConstant
import Interactable.Light.Light as LightConstant
from State.AwakeLightsOffState import AwakeLightsOffState


class DeskState(AwakeLightsOffState):
    id = 5
    name = "Desk"

    def __init__(self, previous_state=None):
        super().__init__(previous_state)
        self.all_lights_on = False

    def execute_state_change(self):
        print("State changed to " + self.name)

        update_db = threading.Thread(self._update_database())
        update_db.start()

        self.current_white = ColorConstant.WHITE_CLOUDY_DAYLIGHT
        self.set_lighting_level(False)

        self.plant_lights.soft_set_on()
        self.oddish_light.soft_set_on()
        self.monitor.set_off()

    # region Button Color

    def get_desk_rear_button_colors(self):
        return [ColorConstant.DIM_GREEN, ColorConstant.GREEN, ColorConstant.BLUE]

    def get_desk_left_button_colors(self):
        return [ColorConstant.DIM_RED, ColorConstant.RED, ColorConstant.BLUE]

    def get_desk_right_button_colors(self):
        return [ColorConstant.DIM_BLUE, ColorConstant.BLUE, ColorConstant.RED]

    # endregion

    # region Button Actions

    def on_primary_long_press(self):
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_desk_left_short_press(self):
        self.set_lighting_level(True)

    def set_lighting_level(self, flip):
        if flip:
            self.all_lights_on = not self.all_lights_on

        if self.all_lights_on:
            LightConstant.all_lamp.turn_on(self.current_white)
        else:
            LightConstant.jaci_bedside_lamp.turn_off()
            LightConstant.entry_lamp.turn_on(self.current_white)
            LightConstant.desk_lamp.turn_on(self.current_white)

    def on_door_short_press(self):
        if self.all_lights_on:
            return AwakeLightsOffState(self)
        else:
            from State.AwakeLightsOnState import AwakeLightsOnState
            return AwakeLightsOnState(self)

    def on_door_long_press(self):
        return AwakeLightsOffState(self)

    # endregion

    # region On Event

    def on_kelvin_changed(self):
        self.set_lighting_level(False)

    # endregion
