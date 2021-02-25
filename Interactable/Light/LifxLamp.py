import threading
import time

from lifxlan import Group

SLEEP_TIME_WHEN_FAIL = 0.1
LIFX_STATE_CHANGE_ATTEMPTS = 5
DEFAULT_TRANSITION_TIME = 200


class LifxLamp():
    def __init__(self, lifx_lights, name):
        self.name = name
        self.lifx_lifx_lights = lifx_lights

    def _group(self, lifx_lights):
        return Group(list(map(lambda l: l.wrapped_bulb, lifx_lights)))

    def turn_on(self, color, transition_time=None):
        self._set_group(color, transition_time)

    def turn_off(self, transition_time=None):
        self._set_group(None, transition_time)

    def can_handle_kelvin(self):
        return True

    def _get_transition_time(self, transition_time):
        return DEFAULT_TRANSITION_TIME if transition_time is None else transition_time

    def _set_group(self, color, transition_time):
        on_group = self._group(list(filter(lambda x: x.get_is_on(), self.lifx_lifx_lights)))
        off_group = self._group(list(filter(lambda x: not x.get_is_on(), self.lifx_lifx_lights)))
        turn_off = color is None

        if turn_off:
            threading.Thread(target=self._turn_off, args=(on_group, transition_time)).start()
        else:
            threading.Thread(target=self._turn_on, args=(on_group, off_group, color, transition_time)).start()

    def _turn_on(self, on_group, off_group, color, transition_time):
        transition_time = self._get_transition_time(transition_time)

        # Since the lights are already off the color can be changed and nothing will happen in the room
        for x in range(LIFX_STATE_CHANGE_ATTEMPTS):
            try:
                off_group.set_color(color.as_hsv_array(), 0)
            except:
                time.sleep(SLEEP_TIME_WHEN_FAIL)
            else:
                break

        # Take all of the lights that are off and turn them on. They already have the right color set.
        for x in range(LIFX_STATE_CHANGE_ATTEMPTS):
            try:
                off_group.set_power(True, transition_time)
            except:
                time.sleep(SLEEP_TIME_WHEN_FAIL)
            else:
                break

        # Change the color in the lights that were previously on.
        for x in range(LIFX_STATE_CHANGE_ATTEMPTS):
            try:
                on_group.set_color(color.as_hsv_array(), transition_time)
            except:
                time.sleep(SLEEP_TIME_WHEN_FAIL)
            else:
                break

        # Update each light's state for future reference.
        for light in self.lifx_lifx_lights:
            light.is_off = False
            light.current_color = color

    def _turn_off(self, group, transition_time):
        transition_time = self._get_transition_time(transition_time)

        # In this case we only care about the lights that are on and all we need to do is turn them off.
        for x in range(LIFX_STATE_CHANGE_ATTEMPTS):
            try:
                group.set_power(False, transition_time)
                self.is_off = True
            except:
                time.sleep(SLEEP_TIME_WHEN_FAIL)
            else:
                break

        # Update each light's state for future reference.
        for light in self.lifx_lifx_lights:
            light.is_off = True
            light.current_color = None
