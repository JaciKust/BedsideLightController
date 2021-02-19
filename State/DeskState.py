import Color as ColorConstant
import Interactable.Light.Light as LightConstant
from State.AwakeLightsOffState import AwakeLightsOffState


class DeskState(AwakeLightsOffState):
    def __init__(self, previous_state=None):
        super().__init__(previous_state)
        self.all_lights_on = False

    def get_desk_rear_button_colors(self):
        return [ColorConstant.GREEN, ColorConstant.DARK_GREEN, ColorConstant.WHITE_NEUTRAL]

    def get_desk_left_button_colors(self):
        return [ColorConstant.RED, ColorConstant.DARK_RED, ColorConstant.WHITE_NEUTRAL]

    def execute_state_change(self):
        print("State changed to " + self.name)
        self._update_database()
        self.current_white = ColorConstant.WHITE_CLOUDY_DAYLIGHT
        self.set_lighting_level(False)

        self.plant_lights.set_off()
        self.oddish_light.set_on()
        self.monitor.set_off()

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

    def on_kelvin_changed(self):
        self.set_lighting_level(False)
