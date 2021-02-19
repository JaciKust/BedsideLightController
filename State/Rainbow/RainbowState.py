from time import sleep

import Color as ColorConstant
import Interactable.Light.Light as LightConstant
from State.Rainbow import BaseLightPattern
from State.Rainbow import PatternType
from State.Rainbow.LightShow import LightShow
from State.Rainbow.OneLightShow import OneLightShow
from State.Rainbow.RandomLightShow import RandomLightShow
from State.State import State


class RainbowState(State):
    id = 40
    name = 'Rainbow'

    def __init__(self):
        super().__init__(None)
        self.light_show = None

        self.current_pattern = self.DEFAULT_PATTERN_LOCATION
        self.current_speed = self.DEFAULT_SPEED_LOCATION
        self.current_wait = self.DEFAULT_WAIT_LOCATION

        self._update_light_show()

    def __del__(self):
        self._stop_current_light_show()

    def execute_state_change(self):
        LightConstant.all_lamp.turn_on(ColorConstant.MAGENTA)
        self.plant_lights.set_off()
        self.oddish_light.set_off()
        self.fan.set_off()
        self.monitor.set_off()

    # region Button Color

    def get_primary_button_colors(self):
        return [ColorConstant.MAGENTA, ColorConstant.DARK_MAGENTA, ColorConstant.RED]

    def get_door_button_colors(self):
        return [ColorConstant.BLACK, ColorConstant.BLACK, ColorConstant.BLACK]

    def get_secondary_button_colors(self):
        return [ColorConstant.CYAN, ColorConstant.DARK_CYAN, ColorConstant.BLUE]

    # endregion

    # region Pattern

    DEFAULT_PATTERN_LOCATION = 0

    def _cycle_pattern(self):
        self.current_pattern += 1
        self.current_pattern %= len(BaseLightPattern.patterns)
        print("Current pattern: " + str(self._get_pattern().name))

    def _get_pattern(self):
        return BaseLightPattern.patterns[self.current_pattern]

    # endregion

    # region Speed

    DEFAULT_SPEED_LOCATION = 3
    speeds = [1, 2, 5, 10, 15, 20, 30]

    def _cycle_speed(self):
        self.current_speed += 1
        self.current_speed %= len(self.speeds)
        print("Current speed: " + str(self._get_speed()))

    def _get_speed(self):
        return self.speeds[self.current_speed]

    # endregion

    # region Wait

    DEFAULT_WAIT_LOCATION = 0
    waits = [0, 1, 5, 15, 30]

    def _cycle_wait(self):
        self.current_wait += 1
        self.current_wait %= len(self.waits)
        print("Current wait: " + str(self._get_wait()))

    def _get_wait(self):
        return self.waits[self.current_wait]

    # endregion

    # region Light Show

    def _stop_current_light_show(self):
        if self.light_show is not None:
            self.light_show.stop_if_necessary()
            while True:
                sleep(0.5)
                if self.light_show.is_stopped():
                    break

    def _update_light_show(self):
        self._stop_current_light_show()
        pattern_type = self._get_pattern().pattern
        if pattern_type == PatternType.BASE:
            self.light_show = LightShow(self._get_pattern(), self._get_speed(), self._get_wait())
        elif pattern_type == PatternType.ONE:
            self.light_show = OneLightShow(self._get_pattern(), self._get_speed(), self._get_wait())
        elif pattern_type == PatternType.RANDOM:
            self.light_show = RandomLightShow(self._get_pattern(), self._get_speed(), self._get_wait())

        self.light_show.start()

    # endregion

    # region Button Actions

    def on_primary_short_press(self):
        self._cycle_pattern()
        self._update_light_show()

    def on_primary_long_press(self):
        self._cycle_wait()
        self._update_light_show()

    def on_primary_extra_long_press(self):
        self._stop_current_light_show()
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState()

    def on_secondary_short_press(self):
        self._cycle_speed()
        self._update_light_show()

    def on_secondary_long_press(self):
        self._stop_current_light_show()
        return RainbowState()

    # These all exit back to lights on.

    def on_secondary_extra_long_press(self):
        return self.on_primary_extra_long_press()

    def on_door_short_press(self):
        return self.on_primary_extra_long_press()

    def on_door_long_press(self):
        return self.on_primary_extra_long_press()

    def on_door_extra_long_press(self):
        return self.on_primary_extra_long_press()

    def on_desk_rear_short_press(self):
        return self.on_primary_extra_long_press()

    def on_desk_rear_long_press(self):
        return self.on_primary_extra_long_press()

    def on_desk_rear_extra_long_press(self):
        return self.on_primary_extra_long_press()

    # endregion
