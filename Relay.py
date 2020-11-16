from RPi import GPIO

from Toggleable import Toggleable


class Relay(Toggleable):
    def __init__(self, database_id, pin):
        super().__init__(database_id)

        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    def _execute_set_on(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.is_on = True

    def _execute_set_off(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.is_on = False
