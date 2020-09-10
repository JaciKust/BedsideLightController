import colorsys

from lifxlan import LightSetPower

import ColorConstants


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

    def execute_state_change(self, lights):
        pass

    def on_time_expire(self):
        pass

    def __eq__(self, other):
        return other.get_state_identifier() == self.get_state_identifier()

    def __ne__(self, other):
        return not self.__eq__(other)

    def _rgb_to_hsv(self, rgb_color, temperature=3500):
        r = rgb_color[ColorConstants.RED_LOCATION] / 100.0
        g = rgb_color[ColorConstants.GREEN_LOCATION] / 100.0
        b = rgb_color[ColorConstants.BLUE_LOCATION] / 100.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return [h * 65535, s * 65535, v * 65535, temperature]

    def _set_lights(self, lights, color, transition_time):
        color = self._rgb_to_hsv(color)
        for light in lights:
            light.set_color(color, transition_time)
