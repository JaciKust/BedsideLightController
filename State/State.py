import colorsys
import time

from Constants import Color as ColorConstant


class State:
    def __init__(self, id, name, ring_color, on_press_ring_color, on_long_press_ring_color, previous_state):
        self.id = id
        self.name = name
        self.ring_color = ring_color
        self.on_press_ring_color = on_press_ring_color
        self.on_long_press_ring_color = on_long_press_ring_color
        self.previous_state = previous_state

    def on_short_press(self):
        pass

    def on_long_press(self):
        pass

    def on_extra_long_press(self):
        pass

    def get_ring_color(self):
        return self.ring_color

    def get_ring_color_on_press(self):
        return self.on_press_ring_color

    def get_ring_color_on_long_press(self):
        return self.on_long_press_ring_color

    def get_state_name(self):
        return self.name

    def get_state_identifier(self):
        return self.id

    def execute_state_change(self):
        pass

    def on_time_expire_check(self):
        pass

    def __eq__(self, other):
        return other.get_state_identifier() == self.get_state_identifier()

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
