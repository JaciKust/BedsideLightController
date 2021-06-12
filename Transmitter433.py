from datetime import timedelta

from RPi import GPIO

from Constants import Transmitter as TransmitterConstant
from Interactable.OutletSwitch import OutletSwitch


class Transmitter433:
    def __init__(self):
        GPIO.setup(TransmitterConstant.PIN, GPIO.OUT)
        self.fan = OutletSwitch(
            TransmitterConstant.OUTLET_1_ID,
            TransmitterConstant.OUTLET_1_CODES,
            TransmitterConstant.PIN,
            TransmitterConstant.ONE_HIGH_TIME,
            TransmitterConstant.ONE_LOW_TIME,
            TransmitterConstant.ZERO_HIGH_TIME,
            TransmitterConstant.ZERO_LOW_TIME,
            TransmitterConstant.INTERVAL
        )

        self.plant_lights = OutletSwitch(
            TransmitterConstant.OUTLET_2_ID,
            TransmitterConstant.OUTLET_2_CODES,
            TransmitterConstant.PIN,
            TransmitterConstant.ONE_HIGH_TIME,
            TransmitterConstant.ONE_LOW_TIME,
            TransmitterConstant.ZERO_HIGH_TIME,
            TransmitterConstant.ZERO_LOW_TIME,
            TransmitterConstant.INTERVAL,
            timedelta(hours=14)
        )

        self.monitors = OutletSwitch(
            TransmitterConstant.OUTLET_4_ID,
            TransmitterConstant.OUTLET_4_CODES,
            TransmitterConstant.PIN,
            TransmitterConstant.ONE_HIGH_TIME,
            TransmitterConstant.ONE_LOW_TIME,
            TransmitterConstant.ZERO_HIGH_TIME,
            TransmitterConstant.ZERO_LOW_TIME,
            TransmitterConstant.INTERVAL
        )
