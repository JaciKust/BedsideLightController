import ColorConstants
from State import State


class AwakeLightsOnState(State):
    id = 4
    name = 'Awake Lights On'
    ring_color = ColorConstants.WHITE
    on_press_ring_color = ColorConstants.DIM_WHITE
    on_long_press_ring_color = ColorConstants.BLUE

    def __init__(self, previous_state=None):
        super().__init__(self.id, self.name, self.ring_color, self.on_press_ring_color, self.on_long_press_ring_color, previous_state)

    def on_short_press(self):
        from AwakeLightsOffState import AwakeLightsOffState
        return AwakeLightsOffState(self)

    def on_long_press(self):
        from AsleepLightsOffState import AsleepLightsOffState
        return AsleepLightsOffState(self)

    def on_extra_long_press(self):
        return self

    def execute_state_change(self, lights):
        print('changed to: ' + self.name)
        from AsleepLightsOffState import AsleepLightsOffState
        from AsleepLightsOnState import AsleepLightsOnState
        transition_time = 0
        if isinstance(self.previous_state, AsleepLightsOffState) or \
                isinstance(self.previous_state, AsleepLightsOnState):
            transition_time = 10_000
        self._set_lights(lights, ColorConstants.WHITE, transition_time)


    def on_time_expire(self):
        return self
