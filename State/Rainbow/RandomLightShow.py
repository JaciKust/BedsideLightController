import random
import time

from State.Rainbow.LightShow import LightShow


class RandomLightShow(LightShow):
    def __init__(self, light_pattern, transition_time, stop_time):
        super().__init__(light_pattern, transition_time, stop_time)

    def run(self):
        overt = 1000 * self.transition_time
        while True:
            if self._should_stop:
                break
            for light in self.lights:
                light.turn_on(random.choice(self.colors), overt)
            time.sleep(self.transition_time)
            time.sleep(self.stop_time)
