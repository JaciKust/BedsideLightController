import colorsys
import time

from lifxlan import Group

from Constants import Button as ButtonConstant
from Constants import Color as ColorConstant
from Constants import DoorButton as DoorButtonConstant
from Constants import PrimaryButton as PrimaryButtonConstant
from Constants import Relay as RelayConstant
from Constants import SecondaryButton as SecondaryButtonConstant
from Relay import Relay
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

    def get_primary_button_colors(self):
        raise NotImplemented('Getting the primary button color is not implemented for class ' + self.name)

    def get_secondary_button_colors(self):
        return [ColorConstant.BLUE, ColorConstant.GREEN, ColorConstant.RED]

    def get_door_button_colors(self):
        return [ColorConstant.BLACK, ColorConstant.BLACK, ColorConstant.BLACK]

    def on_primary_short_press(self):
        return None

    def on_primary_long_press(self):
        return None

    def on_primary_extra_long_press(self):
        return None

    def execute_state_change(self):
        pass

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

    def get_state_for(self, button, button_time):
        if button.name == PrimaryButtonConstant.NAME:
            return self.get_state_for_primary_button(button_time)

        if button.name == SecondaryButtonConstant.NAME:
            return self.get_state_for_secondary_button(button_time)

        if button.name == DoorButtonConstant.NAME:
            return self.get_state_for_door_button(button_time)

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

    def __eq__(self, other):
        return other.id == self.id

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return self.name

    def _rgb_to_hsv(self, rgb_color, temperature=3500):
        r = rgb_color[ColorConstant.RED_LOCATION] / 100.0
        g = rgb_color[ColorConstant.GREEN_LOCATION] / 100.0
        b = rgb_color[ColorConstant.BLUE_LOCATION] / 100.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return [h * 65535, s * 65535, v * 65535, temperature]

    def _set_lights(self, group, color, transition_time):
        color = self._rgb_to_hsv(color)
        try:
            group.set_color(color, transition_time)
        except:
            print('. Failed Once')
            time.sleep(0.1)
            try:
                group.set_color(color, transition_time)
            except:
                print('.. Failed Twice')
                time.sleep(0.1)
                try:
                    group.set_color(color, transition_time)
                except:
                    print('... Failed Three Times')
                    pass

    def _set_light(self, light, color, transition_time):
        self._set_lights(Group([light]), color, transition_time)
