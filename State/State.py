import colorsys
import logging

from lifxlan import Group

from Constants import Button as ButtonConstant
from Constants import Color as ColorConstant
from Constants import DeskButton as DeskButtonConstant
from Constants import DoorButton as DoorButtonConstant
from Constants import Light as LightConstant
from Constants import PrimaryButton as PrimaryButtonConstant
from Constants import Relay as RelayConstant
from Constants import SecondaryButton as SecondaryButtonConstant
from Relay import Relay
from Sql.MarraQueryMaker import MarraQueryMaker
from Transmitter433 import Transmitter433


class State:
    name = 'Base State'
    id = -1

    def __init__(self, previous_state):
        self.previous_state = previous_state

        transmitter433 = Transmitter433()
        self.fan = transmitter433.fan
        self.monitor = transmitter433.monitor
        self.plant_lights = transmitter433.plant_lights

        self.oddish_light = Relay(RelayConstant.ID, RelayConstant.ODDISH_RELAY_PIN)

        self.maker = MarraQueryMaker.getInstance()
        self.maker.open_connection()

        self.default_transition_time = 200
        self.default_temperature = 3500

    def get_primary_button_colors(self):
        raise NotImplemented('Getting the primary button color is not implemented for class ' + self.name)

    def get_secondary_button_colors(self):
        return [ColorConstant.BLUE, ColorConstant.GREEN, ColorConstant.RED]

    def get_door_button_colors(self):
        return [ColorConstant.BLACK, ColorConstant.BLACK, ColorConstant.BLACK]

    def get_desk_right_button_colors(self):
        return self.get_secondary_button_colors()

    def get_desk_left_button_colors(self):
        return self.get_primary_button_colors()

    def get_desk_rear_button_colors(self):
        return [ColorConstant.BLACK, ColorConstant.BLACK, ColorConstant.BLACK]

    def on_primary_short_press(self):
        return None

    def on_primary_long_press(self):
        return None

    def on_primary_extra_long_press(self):
        return None

    def on_desk_right_short_press(self):
        return self.on_secondary_short_press()

    def on_desk_right_long_press(self):
        return self.on_secondary_long_press()

    def on_desk_right_extra_long_press(self):
        return self.on_secondary_extra_long_press()

    def on_desk_left_short_press(self):
        return self.on_primary_short_press()

    def on_desk_left_long_press(self):
        return self.on_primary_long_press()

    def on_desk_left_extra_long_press(self):
        return self.on_primary_extra_long_press()

    def on_desk_rear_short_press(self):
        return None

    def on_desk_rear_long_press(self):
        return None

    def on_desk_rear_extra_long_press(self):
        return None

    def execute_state_change(self):
        print("State changed to " + self.name)
        self._update_database()

    def on_time_expire_check(self):
        return None

    def on_secondary_short_press(self):
        self.fan.toggle()
        return None

    def on_secondary_long_press(self):
        self.plant_lights.toggle()
        if self.plant_lights.get_is_on():
            self.oddish_light.set_on()
        else:
            self.oddish_light.set_off()
        return None

    def on_secondary_extra_long_press(self):
        self.monitor.toggle()
        return None

    def on_door_short_press(self):
        return None

    def on_door_long_press(self):
        return None

    def on_door_extra_long_press(self):
        return None

    def get_state_for(self, button_name, press_time):
        if button_name == PrimaryButtonConstant.NAME:
            return self.get_state_for_primary_button(press_time)

        if button_name == SecondaryButtonConstant.NAME:
            return self.get_state_for_secondary_button(press_time)

        if button_name == DoorButtonConstant.NAME:
            return self.get_state_for_door_button(press_time)

        if button_name == DeskButtonConstant.RIGHT:
            return self.get_state_for_desk_right(press_time)

        if button_name == DeskButtonConstant.LEFT:
            return self.get_state_for_desk_left(press_time)

        if button_name == DeskButtonConstant.REAR:
            return self.get_state_for_desk_rear(press_time)

        logging.error("Could not determine button name.")

    def get_state_for_primary_button(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_primary_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_primary_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_primary_short_press()
        return return_state

    def get_state_for_secondary_button(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_secondary_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_secondary_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_secondary_short_press()
        return return_state

    def get_state_for_door_button(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_door_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_door_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_door_short_press()
        return return_state

    def get_state_for_desk_right(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_desk_right_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_desk_right_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_desk_right_short_press()
        return return_state

    def get_state_for_desk_left(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_desk_left_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_desk_left_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_desk_left_short_press()
        return return_state

    def get_state_for_desk_rear(self, button_time):
        return_state = None

        # extra long press
        if button_time >= ButtonConstant.EXTRA_LONG_PRESS_MIN:
            return_state = self.on_desk_rear_extra_long_press()

        # long button press
        elif button_time >= ButtonConstant.LONG_PRESS_MIN:
            return_state = self.on_desk_rear_long_press()

        # short press
        elif button_time >= ButtonConstant.NOISE_THRESHOLD:
            return_state = self.on_desk_rear_short_press()

        return return_state

    def __eq__(self, other):
        return other.id == self.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name

    def _rgb_to_hsv(self, rgb_color, temperature):
        r = rgb_color[ColorConstant.RED_LOCATION] / 100.0
        g = rgb_color[ColorConstant.GREEN_LOCATION] / 100.0
        b = rgb_color[ColorConstant.BLUE_LOCATION] / 100.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return [h * 65535, s * 65535, v * 65535, temperature]

    def get_transition_time(self, time):
        return self.default_transition_time if time is None else time

    def get_temperature(self, temp):
        return self.default_temperature if temp is None else temp

    def set_all_lights_off(self, transition_time=None, temperature=None):
        self._set_lights(LightConstant.all_group, ColorConstant.BLACK, transition_time, temperature)

    def set_all_lights_on(self, transition_time=None, temperature=None):
        self._set_lights(LightConstant.all_group, ColorConstant.WHITE, transition_time, temperature)

    def set_lights_on(self, group, transition_time=None, temperature=None):
        self._set_lights(group, ColorConstant.WHITE, transition_time, temperature)

    def set_lights_off(self, group, transition_time=None, temperature=None):
        self._set_lights(group, ColorConstant.BLACK, transition_time, temperature)

    def _set_lights(self, group, color, transition_time=None, temperature=None):
        transition_time = self.get_transition_time(transition_time)
        temperature = self.get_temperature(temperature)
        color = self._rgb_to_hsv(color, temperature)
        num_tries = 5
        for x in range(num_tries):
            try:
                group.set_color(color, transition_time)
            except:
                print("failed {} time to set light".format(x + 1))
            else:
                break

    def _set_light(self, light, color, transition_time, temperature=3500):
        self._set_lights(Group([light]), color, transition_time, temperature)

    def _update_database(self):
        try:
            self.maker.insert_state_status(self.id)
        except:
            print("Unable to update database state for " + str(self.id))
            pass
