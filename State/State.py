import colorsys
import time

from lifxlan import Group

from Constants import Color as ColorConstant


class State:
    name = 'Base State'

    def __init__(self, previous_state):
        self.previous_state = previous_state

    def get_primary_button_colors(self):
        raise NotImplemented('Getting the primary button color is not implemented for class ' + self.name)

    def get_secondary_button_colors(self):
        return [ColorConstant.BLACK, ColorConstant.BLACK, ColorConstant.BLACK]
        # raise NotImplemented('Getting the secondary button color is not implemented for class ' + self.name)

    def get_door_button_colors(self):
        return [ColorConstant.BLACK, ColorConstant.BLACK, ColorConstant.BLACK]
        # raise NotImplemented('Getting the door button color is not implemented for class ' + self.name)

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
        return None

    def on_secondary_long_press(self):
        return None

    def on_secondary_extra_long_press(self):
        return None

    def on_door_short_press(self):
        return None

    def on_door_long_press(self):
        return None

    def on_door_extra_long_press(self):
        return None

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
