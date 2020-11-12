from RPi import GPIO


class Relay:
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(self.pin, GPIO.OUT)

    is_on = False

    def turn_on(self):
        GPIO.output(self.pin, GPIO.LOW)
        self.is_on = True

    def turn_off(self):
        GPIO.output(self.pin, GPIO.HIGH)
        self.is_on = False

    def toggle(self):
        if self.is_on:
            self.turn_off()
        else:
            self.turn_on()
