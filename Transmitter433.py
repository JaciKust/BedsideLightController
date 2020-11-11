import time

from RPi import GPIO

from Constants import Transmitter as TransmitterConstant


class Transmitter433:
    def __init__(self):
        GPIO.setup(TransmitterConstant.PIN, GPIO.OUT)

    def _send_code(self, code):
        for i in range(10):
            for bit in code:
                if int(bit) == GPIO.HIGH:
                    GPIO.output(TransmitterConstant.PIN, GPIO.HIGH)
                    time.sleep(TransmitterConstant.ONE_HIGH_TIME)
                    GPIO.output(TransmitterConstant.PIN, GPIO.LOW)
                    time.sleep(TransmitterConstant.ONE_LOW_TIME)
                else:
                    GPIO.output(TransmitterConstant.PIN, GPIO.HIGH)
                    time.sleep(TransmitterConstant.ZERO_HIGH_TIME)
                    GPIO.output(TransmitterConstant.PIN, GPIO.LOW)
                    time.sleep(TransmitterConstant.ZERO_LOW_TIME)
            GPIO.output(TransmitterConstant.PIN, GPIO.LOW)
            time.sleep(TransmitterConstant.INTERVAL)

    def turn_1_on(self):
        self._send_code(TransmitterConstant.OUTLET_1_CODES[TransmitterConstant.ON_LOCATION])

    def turn_1_off(self):
        self._send_code(TransmitterConstant.OUTLET_1_CODES[TransmitterConstant.OFF_LOCATION])

    def turn_2_on(self):
        self._send_code(TransmitterConstant.OUTLET_2_CODES[TransmitterConstant.ON_LOCATION])

    def turn_2_off(self):
        self._send_code(TransmitterConstant.OUTLET_2_CODES[TransmitterConstant.OFF_LOCATION])

    def turn_3_on(self):
        self._send_code(TransmitterConstant.OUTLET_3_CODES[TransmitterConstant.ON_LOCATION])

    def turn_3_off(self):
        self._send_code(TransmitterConstant.OUTLET_3_CODES[TransmitterConstant.OFF_LOCATION])

    def turn_4_on(self):
        self._send_code(TransmitterConstant.OUTLET_4_CODES[TransmitterConstant.ON_LOCATION])

    def turn_4_off(self):
        self._send_code(TransmitterConstant.OUTLET_4_CODES[TransmitterConstant.OFF_LOCATION])

    def turn_5_on(self):
        self._send_code(TransmitterConstant.OUTLET_5_CODES[TransmitterConstant.ON_LOCATION])

    def turn_5_off(self):
        self._send_code(TransmitterConstant.OUTLET_5_CODES[TransmitterConstant.OFF_LOCATION])
