import TimeFunctions
from Constants import Color as ColorConstant
from Constants import Light as LightConstant
from Constants import Time as TimeConstant
from State.State import State


class AwakeLightsOnState(State):
    id = 4
    name = 'Awake Lights On'

    def __init__(self, previous_state=None):
        super().__init__(previous_state)

    def get_primary_button_colors(self):
        return [ColorConstant.WHITE, ColorConstant.DIM_WHITE, ColorConstant.BLUE]

    def get_door_button_colors(self):
        return [ColorConstant.WHITE, ColorConstant.DIM_WHITE, ColorConstant.BLACK]

    def on_primary_short_press(self):
        from State.AwakeLightsOffState import AwakeLightsOffState
        return AwakeLightsOffState(self)

    def on_primary_long_press(self):
        from State.AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(TimeFunctions.get_next(TimeConstant.wakeup_time), self)

    def on_primary_extra_long_press(self):
        from State.CyanCustomState import CyanCustomState
        return CyanCustomState()

    def on_door_short_press(self):
        return self.on_primary_short_press()

    def execute_state_change(self):
        print('changed to: ' + self.name)
        from State.AsleepLightsOffState import AsleepLightsOffState
        from State.AsleepLightsOnState import AsleepLightsOnState
        transition_time = 1_000
        self._turn_off_fan()
        if isinstance(self.previous_state, AsleepLightsOffState) or \
                isinstance(self.previous_state, AsleepLightsOnState):
            transition_time = 10_000
        self._set_lights(LightConstant.all_group, ColorConstant.WHITE, transition_time)
        self._turn_on_plant_lights()
        self._turn_on_oddish_light()
