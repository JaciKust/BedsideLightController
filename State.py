class State:
    def __init__(self, id, name):
        self.id = id
        self.name = name

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

    def get_state_name(self):
        return self.name

    def get_state_identifier(self):
        return self.id

    def __eq__(self, other):
        return other.get_state_identifier() == self.get_state_identifier()

