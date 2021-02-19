import threading

from lifxlan import Group


# import Interactable.Light.Lamp as Lamp

class LifxLamp():
    def __init__(self, lifx_lights, name):
        self.name = name
        self.wrapped_lights = self._get_wrapped_lights(lifx_lights)
        self.lifx_lifx_lights = lifx_lights
        self.group = Group(self.wrapped_lights)
        self.current_color = None
        self.is_off = True

    default_transition_time = 200

    def _get_wrapped_lights(self, lifx_lights):
        return list(map(lambda l: l.wrapped_bulb, lifx_lights))

    def turn_on(self, color, transition_time=None):
        self._set_group(color, transition_time)

    def turn_off(self, transition_time=None):
        self._set_group(None, transition_time)

    def get_is_on(self):
        return not self.is_off

    def get_current_color(self):
        return self.current_color

    def can_handle_kelvin(self):
        return True

    def _get_transition_time(self, time):
        return self.default_transition_time if time is None else time

    def _set_group(self, color, transition_time):
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
                    self.group.set_power(False, transition_time)
                    self.is_off = True
                else:
                    if self.is_off:
                        self.group.set_color(color.as_hsv_array(), 0)
                        self.group.set_power(True, transition_time)
                        self.is_off = False
                    else:
                        self.group.set_color(color.as_hsv_array(), transition_time)
            except:
                pass
            else:
                break
