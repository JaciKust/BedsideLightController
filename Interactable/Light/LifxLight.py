import threading

from lifxlan import Light as Lifx

import Color as ColorConstant

BRAND = "LIFX"
CATEGORY = "A19 1100lm"


class LifxLight():
    def __init__(self, mac_address, ip_address, name):
        self.is_on = False
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.name = name
        self.wrapped_bulb = Lifx(self.mac_address, self.ip_address)

    default_transition_time = 200

    def turn_on(self, color, transition_time=None):
        try:
            self._set_lights(color, transition_time)
        finally:
            self.is_on = True

    def turn_off(self, transition_time=None):
        try:
            self._set_lights(ColorConstant.BLACK, transition_time)
        finally:
            self.is_on = False

    def get_is_on(self):
        return self.is_on

    def can_handle_kelvin(self):
        return True

    def _get_transition_time(self, time):
        return self.default_transition_time if time is None else time

    def _set_lights(self, color, transition_time):
        threading.Thread(target=self._run, args=(color, transition_time)).start()

    def _run(self, color, transition_time):
        transition_time = self._get_transition_time(transition_time)
        num_tries = 5
        for x in range(num_tries):
            try:
                self.wrapped_bulb.set_color(color.as_hsv_array(), transition_time)
            except:
                pass
            else:
                break
