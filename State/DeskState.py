import logging

from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from Constants import Light_Temperature as TemperatureConstant
from State.AwakeLightsOffState import AwakeLightsOffState


class DeskState(AwakeLightsOffState):
    def __init__(self, previous_state=None):
        super().__init__(previous_state)
        self.all_lights_on = False
        self.current_temp_int = 3
        self.current_temperature = TemperatureConstant.CYCLE[3]

    def get_desk_rear_button_colors(self):
        return [ColorConstant.GREEN, ColorConstant.DARK_GREEN, ColorConstant.WHITE]

    def get_desk_left_button_colors(self):
        return [ColorConstant.RED, ColorConstant.DARK_RED, ColorConstant.WHITE]

    def execute_state_change(self):
        print("State changed to " + self.name)
        self._update_database()

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
            self.set_all_lights_on(None, self.current_temperature)
        else:
            self.set_lights_off(LightConstant.jaci_bedside_group)
            self.set_lights_on(LightConstant.desk_group, 2000, self.current_temperature)

    def on_door_short_press(self):
        if self.all_lights_on:
            return AwakeLightsOffState(self)
        else:
            from State.AwakeLightsOnState import AwakeLightsOnState
            return AwakeLightsOnState(self)

    def on_door_long_press(self):
        return AwakeLightsOffState(self)

    def on_desk_rear_short_press(self):
        self.cycle_light_temperature()

    def cycle_light_temperature(self):

        self.current_temp_int += 1
        self.current_temp_int %= len(TemperatureConstant.CYCLE)
        self.current_temperature = TemperatureConstant.CYCLE[self.current_temp_int]

        logging.info("Changing temperature to level {}".format(self.current_temp_int))
        logging.info("New Temperature: {}".format(self.current_temperature))
        self.set_lighting_level(False)
