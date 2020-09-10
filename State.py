class State:
    def __init__(self, id, name, ring_color, on_press_ring_color, on_long_press_ring_color, previous_state):
        self.id = id
        self.name = name
        self.ring_color = ring_color
        self.on_press_ring_color = on_press_ring_color
        self.on_long_press_ring_color = on_long_press_ring_color
        self.previous_state = previous_state

    def on_short_press(self):
        pass

    def on_long_press(self):
        pass

    def on_extra_long_press(self):
        pass

    def get_ring_color(self):
        return self.ring_color

    def get_ring_color_on_press(self):
        return self.on_press_ring_color

    def get_ring_color_on_long_press(self):
        return self.on_long_press_ring_color

    def get_state_name(self):
        return self.name

    def get_state_identifier(self):
        return self.id

    def execute_state_change(self):
        pass

    def on_time_expire(self):
        pass

    def __eq__(self, other):
        return other.get_state_identifier() == self.get_state_identifier()

    def __ne__(self, other):
        return not self.__eq__(other)

