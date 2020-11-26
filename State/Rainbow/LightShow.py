import colorsys
import threading
import time

from lifxlan import Group

from Constants import Color as ColorConstant
from State.Rainbow.LightPattern import LightPattern


class LightShow:
    def __init__(self, light_pattern, transition_time, stop_time):
        assert isinstance(light_pattern, LightPattern), \
            "Expected LightShowSetting for light_show_setting but got {}".format(type(light_pattern))
        assert isinstance(transition_time, int), "Expected float for transition_time but got {}".format(
            type(transition_time))
        assert isinstance(stop_time, int), "Expected float for stop_time but got {}".format(type(stop_time))

        self.pattern = light_pattern
        self.lights = light_pattern.lights
        self.colors = light_pattern.colors
        self.transition_time = transition_time
        self.stop_time = stop_time
        self.process = None
        self._should_stop = False

    def __del__(self):
        self.stop_if_necessary()

    def start(self):
        assert self.is_stopped(), "Cannot start the process while it is already running."

        self._should_stop = False
        self.process = threading.Thread(target=self.run)
        self.process.start()

    def stop(self):
        assert not self.is_stopped(), "Cannot stop the process -- it has not been started."

        self._should_stop = True
        self.process = None

    def is_stopped(self):
        return self.process is None

    def stop_if_necessary(self):
        if self.process is not None:
            self.stop()

    def run(self):
        overt = 1000 * self.transition_time
        c = 0
        while True:
            if self._should_stop:
                break
            for light in self.lights:
                self._set_light_array(light, self.colors[c], overt)
                c += 1
                c %= len(self.colors)
            c += 1
            c %= len(self.colors)
            time.sleep(self.transition_time)
            time.sleep(self.stop_time)

    def _rgb_to_hsv(self, rgb_color, temperature=3500):
        r = rgb_color[ColorConstant.RED_LOCATION] / 100.0
        g = rgb_color[ColorConstant.GREEN_LOCATION] / 100.0
        b = rgb_color[ColorConstant.BLUE_LOCATION] / 100.0
        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        return [h * 65535, s * 65535, v * 65535, temperature]

    def _set_lights(self, group, color, transition_time):
        color = self._rgb_to_hsv(color)
        num_tries = 5
        for x in range(num_tries):
            try:
                group.set_color(color, transition_time)
            except:
                pass
                # print("failed {} time to set light".format(x + 1))
            else:
                break

    def _set_light_array(self, lights, color, transition_time):
        self._set_lights(Group(lights), color, transition_time)
