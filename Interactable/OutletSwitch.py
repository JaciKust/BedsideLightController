import threading
import time

from RPi import GPIO

from Constants import Transmitter as TransmitterConstant
from Interactable.Toggleable import Toggleable


class TransmitterLock:
    is_locked = False


class OutletSwitch(Toggleable):
    def __init__(self, database_id, codes, gpio_pin, one_high_time, one_low_time, zero_high_time, zero_low_time,
                 interval, max_time_on=None):
        super().__init__(database_id, max_time_on)
        self.gpio_pin = gpio_pin
        self.one_high_time = one_high_time
        self.one_low_time = one_low_time
        self.zero_high_time = zero_high_time
        self.zero_low_time = zero_low_time
        self.interval = interval
        self._on_code = codes[TransmitterConstant.ON_LOCATION]
        self._off_code = codes[TransmitterConstant.OFF_LOCATION]

    def _execute_set_on(self):
        self._send_code(self._on_code)

    def _execute_set_off(self):
        self._send_code(self._off_code)

    def _send_code(self, code):
        threading.Thread(target=self._run, args=[code, ]).start()

    def _run(self, code):
        while TransmitterLock.is_locked:
            time.sleep(0.01)

        try:
            TransmitterLock.is_locked = True
            for i in range(10):
                for bit in code:
                    if int(bit) == GPIO.HIGH:
                        GPIO.output(self.gpio_pin, GPIO.HIGH)
                        time.sleep(self.one_high_time)
                        GPIO.output(self.gpio_pin, GPIO.LOW)
                        time.sleep(self.one_low_time)
                    else:
                        GPIO.output(self.gpio_pin, GPIO.HIGH)
                        time.sleep(self.zero_high_time)
                        GPIO.output(self.gpio_pin, GPIO.LOW)
                        time.sleep(self.zero_low_time)
                GPIO.output(self.gpio_pin, GPIO.LOW)
                time.sleep(self.interval)
        finally:
            TransmitterLock.is_locked = False
