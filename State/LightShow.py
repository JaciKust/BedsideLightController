import colorsys
import threading
import time

from lifxlan import Group

from Constants import Color as ColorConstant


class LightShow:
    def __init__(self, lights, colors, transition_time, stop_time):
        self.lights = lights
        self.colors = colors
        self.transition_time = transition_time
        self.stop_time = stop_time
        self.process = None
        self._should_stop = False

    def __del__(self):
        self.stop_if_necessary()

    def start(self):
        if self.process is not None:
            raise ("Cannot start the process while it is already running.")

        self._should_stop = False
        self.process = threading.Thread(target=self.run)
        self.process.start()

    def stop(self):
        if self.process is None:
            raise ("Cannot stop the process -- it has not been started.")

        self._should_stop = True
        self.process = None

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
                self._set_light(light, self.colors[c], overt)
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

    def _set_light(self, lights, color, transition_time):
        self._set_lights(Group(lights), color, transition_time)
