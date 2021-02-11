import threading

from lifxlan import Group

import Color as ColorConstant


# import Interactable.Light.Lamp as Lamp

class LifxLamp():
    def __init__(self, lifx_lights, name):
        self.name = name
        self.wrapped_lights = self._get_wrapped_lights(lifx_lights)
        self.lifx_lifx_lights = lifx_lights
        self.group = Group(self.wrapped_lights)

    default_transition_time = 200

    def _get_wrapped_lights(self, lifx_lights):
        return list(map(lambda l: l.wrapped_bulb, lifx_lights))

    def turn_on(self, color, transition_time=None):
        try:
            self._set_group(color, transition_time)
        finally:
            self.is_on = True

    def turn_off(self, transition_time=None):
        try:
            self._set_group(ColorConstant.BLACK, transition_time)
        finally:
            self.is_on = False

    def get_is_on(self):
        return self.is_on

    def can_handle_kelvin(self):
        return True

    def _get_transition_time(self, time):
        return self.default_transition_time if time is None else time

    def _set_group(self, color, transition_time):
        threading.Thread(target=self._run, args=(color, transition_time)).start()

    def _run(self, color, transition_time):
        transition_time = self._get_transition_time(transition_time)
        num_tries = 5
        for x in range(num_tries):
            try:
                self.group.set_color(color.as_hsv_array(), transition_time)
            except:
                pass
            else:
                break
