from State import State


class AsleepLightsOn(State):
    id = 2
    name = 'Asleep Lights On'

    def __init__(self):
        super().__init__(self, self.id, self.name)

    def on_short_press(self):
        pass

    def on_long_press(self):
        pass

    def on_extra_long_press(self):
        pass

    def get_ring_color(self):
        pass

    def get_ring_color_on_press(self):
        pass
