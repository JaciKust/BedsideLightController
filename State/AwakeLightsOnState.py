import threading
import time

import Color as ColorConstant
import Interactable.Light.Light as LightConstant
import TimeFunctions
from Constants import Time as TimeConstant
from State.State import State


class AwakeLightsOnState(State):
    id = 4
    name = 'Awake Lights On'

    def __init__(self, previous_state=None):
        super().__init__(previous_state)

    def execute_state_change(self):
        super().execute_state_change()
        from State.AsleepLightsOffState import AsleepLightsOffState
        from State.AsleepLightsOnState import AsleepLightsOnState

        self.fan.set_off()

        transition_time_ms = 1_000
        if isinstance(self.previous_state, AsleepLightsOffState) or \
                isinstance(self.previous_state, AsleepLightsOnState):
            transition_time_ms = 10_000
        LightConstant.all_lamp.turn_on(self.current_white, transition_time_ms)

        from State.WakingUpState2 import WakingUpState2
        if isinstance(self.previous_state, WakingUpState2):
            self.set_default_white()
        plant_light_thread = threading.Thread(target=self.wait_run_accessories_on, args=(transition_time_ms / 1000,))
        plant_light_thread.start()

    def on_time_check(self):
        super().on_time_check()
        self.plant_lights.set_on_if_under_max_time()
        self.oddish_light.set_on_if_under_max_time()

    run_delayed_accessories = False

    def wait_run_accessories_on(self, transition_time_seconds):
        try:
            self.run_delayed_accessories = True
            time.sleep(transition_time_seconds)

            if not self.run_delayed_accessories:
                return

            self.plant_lights.soft_set_on()

            if not self.run_delayed_accessories:
                return

            self.oddish_light.soft_set_on()

            if not self.run_delayed_accessories:
                return

            self.monitor.set_on()
        finally:
            self.run_delayed_accessories = False

    def stop_delayed_accessories(self):
        self.run_delayed_accessories = False

    def execute_state_leave(self):
        self.stop_delayed_accessories()

    # region Button Colors

    def get_primary_button_colors(self):
        return [ColorConstant.DIM_WHITE, ColorConstant.WHITE_NEUTRAL, ColorConstant.BLUE]

    def get_door_button_colors(self):
        return [ColorConstant.DIM_WHITE, ColorConstant.WHITE_NEUTRAL, ColorConstant.BLACK]

    # endregion

    # region Button Actions

    def on_primary_short_press(self):
        from State.AwakeLightsOffState import AwakeLightsOffState
        return AwakeLightsOffState(self)

    def on_primary_long_press(self):
        from State.AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(TimeFunctions.get_next(TimeConstant.wakeup_time), self)

    def on_primary_extra_long_press(self):
        from State.Rainbow.RainbowState import RainbowState
        return RainbowState()

    def on_desk_left_long_press(self):
        from State.DeskState import DeskState
        return DeskState(self)

    def on_door_short_press(self):
        return self.on_primary_short_press()

    def on_kelvin_changed(self):
        LightConstant.all_lamp.turn_on(self.current_white)
        pass

    # endregion