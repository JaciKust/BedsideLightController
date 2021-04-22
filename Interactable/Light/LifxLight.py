import threading
import time

from lifxlan import Light as Lifx

BRAND = "LIFX"
CATEGORY = "A19 1100lm"

class LifxLight():
    def __init__(self, mac_address, ip_address, name):
        self.is_on = False
        self.mac_address = mac_address
        self.ip_address = ip_address
        self.name = name
        self.wrapped_bulb = Lifx(self.mac_address, self.ip_address)
        self.current_color = None
        self.is_off = True

    default_transition_time = 200

    def turn_on(self, color, transition_time=None):
        self._set_lights(color, transition_time)

    def turn_off(self, transition_time=None):
        self._set_lights(None, transition_time)

    def get_is_on(self):
        return not self.is_off

    def get_current_color(self):
        return self.current_color

    def can_handle_kelvin(self):
        return True

    def _get_transition_time(self, time):
        return self.default_transition_time if time is None else time

    def _set_lights(self, color, transition_time):
        turn_off = color is None
        if not turn_off:
            self.current_color = color
        threading.Thread(target=self._run, args=(color, transition_time, turn_off)).start()

    def _run(self, color, transition_time, turn_off):
        transition_time = self._get_transition_time(transition_time)
        num_tries = 5
        for x in range(num_tries):
            try:
                if turn_off:
                    self.wrapped_bulb.set_power(False, transition_time)
                    self.is_off = True
                else:
                    if self.is_off:
                        self.wrapped_bulb.set_color(color.as_hsv_array(), 0)
                        self.wrapped_bulb.set_power(True, transition_time)
                        self.is_off = False
                    else:
                        self.wrapped_bulb.set_color(color.as_hsv_array(), transition_time)
            except:
                time.sleep(0.1)
            else:
                break

