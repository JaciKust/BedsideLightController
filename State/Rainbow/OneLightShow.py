import time

from State.Rainbow.LightShow import LightShow


class OneLightShow(LightShow):
    def __init__(self, light_pattern, transition_time, stop_time):
        super().__init__(light_pattern, transition_time, stop_time)

    def run(self):
        overt = 1000 * self.transition_time
        c = 0
        while True:
            if self._should_stop:
                break
            self.lights.turn_on(self.colors[c], overt)
            c += 1
            c %= len(self.colors)
            time.sleep(self.transition_time)
            time.sleep(self.stop_time)
