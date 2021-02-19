import Color as ColorConstant
import Interactable.Light.Light as LightConstant
import TimeFunctions
from Constants import Time as TimeConstant
from State.State import State

class AwakeLightsOffState(State):
    id = 3
    name = 'Awake Lights Off'
    ring_color = ColorConstant.MEDIUM_WHITE
    on_press_ring_color = ColorConstant.DIM_WHITE
    on_long_press_ring_color = ColorConstant.BLUE

    def __init__(self, previous_state=None):
        super().__init__(previous_state)

    def execute_state_change(self):
        super().execute_state_change()
        LightConstant.all_lamp.turn_off(1000)

        self.plant_lights.set_on()
        self.fan.set_off()
        self.oddish_light.set_on()
        self.monitor.set_off()

    # region Button Color

    def get_primary_button_colors(self):
        return [ColorConstant.MEDIUM_WHITE, ColorConstant.DIM_WHITE, ColorConstant.BLUE]

    def get_door_button_colors(self):
        return [ColorConstant.MEDIUM_WHITE, ColorConstant.DIM_WHITE, ColorConstant.BLACK]

    # endregion

    # region Button Actions

    def on_primary_short_press(self):
        from State.AwakeLightsOnState import AwakeLightsOnState
        return AwakeLightsOnState(self)

    def on_primary_long_press(self):
        from State.AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(TimeFunctions.get_next(TimeConstant.wakeup_time), self)

    def on_primary_extra_long_press(self):
        from State.Rainbow.RainbowState import RainbowState
        return RainbowState()

    def on_door_short_press(self):
        return self.on_primary_short_press()

    # endregion
