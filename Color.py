import colorsys

from Constants import LightKelvin as LightKelvinConstant


class Color:

    def __init__(self, red, green, blue, kelvin=LightKelvinConstant.NEUTRAL):
        self.red = red
        self.green = green
        self.blue = blue
        self.kelvin = kelvin
        self._calc_hsv()

    hue = None
    saturation = None
    value = None

    def _calc_hsv(self):
        r = self.red / 100.0
        g = self.green / 100.0
        b = self.blue / 100.0

        h, s, v = colorsys.rgb_to_hsv(r, g, b)
        multiplier = 65535
        self.hue = h * multiplier
        self.saturation = s * multiplier
        self.value = v * multiplier

    def as_rgb_array(self):
        return [
            self.red,
            self.green,
            self.blue,
            self.kelvin
        ]

    def as_hsv_array(self):
        return [
            self.hue,
            self.saturation,
            self.value,
            self.kelvin
        ]


def get_white(temperature):
    return Color(100, 100, 100, temperature)


WHITE = get_white(LightKelvinConstant.NEUTRAL)
COLD_WHITE = get_white(LightKelvinConstant.BLUE_ICE)
HOT_WHITE = get_white(LightKelvinConstant.ULTRA_WARM)

BLACK = Color(0, 0, 0)

RED = Color(100, 0, 0)
GREEN = Color(0, 100, 0)
BLUE = Color(0, 0, 100)

DARK_CYAN = Color(0, 1, 1)
DARK_MAGENTA = Color(1, 0, 1)
DARK_YELLOW = Color(1, 0, 0)

CYAN = Color(0, 100, 100)
MAGENTA = Color(100, 0, 100)
YELLOW = Color(100, 100, 0)

DIM_WHITE = Color(3, 5, 5)
MEDIUM_WHITE = Color(20, 20, 20)

DARK_BLUE = Color(0, 0, 1)
DARK_RED = Color(1, 0, 0)
DARK_GREEN = Color(0, 1, 0)

DIM_MAGENTA = Color(20, 0, 20)

DIMMEST_WHITE = Color(0.1, 0.1, 0.1)

PRIMARIES = [
    RED,
    GREEN,
    BLUE,
]

TWOS = [
    CYAN,
    MAGENTA,
    YELLOW,
]
