import adafruit_pca9685
import board
import busio

FREQUENCY = 600


class PwmHat:
    def __init__(self):
        i2c = busio.I2C(board.SCL, board.SDA)
        self.hat = adafruit_pca9685.PCA9685(i2c)
        self.hat.frequency = FREQUENCY

    def get_color(self, c):
        return int((100 - c) / 100 * 65535)

    def set_color(self, channel, percentage):
        p = self.get_color(percentage)
        c = self.hat.channels[channel]
        c.duty_cycle = p


default_i2c_hat = PwmHat()
