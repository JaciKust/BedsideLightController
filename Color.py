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

DIM_WHITE = Color(1, 1, 1)
MEDIUM_WHITE = Color(20, 20, 20)

DARK_BLUE = Color(0, 0, 1)
DARK_RED = Color(1, 0, 0)
DARK_GREEN = Color(0, 1, 0)

DIM_MAGENTA = Color(20, 0, 20)

DIMMEST_WHITE = Color(0.1, 0.1, 0.1)

# region All Whites

WHITE_ULTRA_WARM = get_white(LightKelvinConstant.ULTRA_WARM)
WHITE_INCANDESCENT = get_white(LightKelvinConstant.INCANDESCENT)
WHITE_WARM = get_white(LightKelvinConstant.WARM)
WHITE_NEUTRAL_WARM = get_white(LightKelvinConstant.NEUTRAL_WARM)
WHITE_NEUTRAL = get_white(LightKelvinConstant.NEUTRAL)
WHITE_COOL = get_white(LightKelvinConstant.COOL)
WHITE_COOL_DAYLIGHT = get_white(LightKelvinConstant.COOL_DAYLIGHT)
WHITE_SOFT_DAYLIGHT = get_white(LightKelvinConstant.SOFT_DAYLIGHT)
WHITE_DAYLIGHT = get_white(LightKelvinConstant.DAYLIGHT)
WHITE_NOON_DAYLIGHT = get_white(LightKelvinConstant.NOON_DAYLIGHT)
WHITE_BRIGHT_DAYLIGHT = get_white(LightKelvinConstant.BRIGHT_DAYLIGHT)
WHITE_CLOUDY_DAYLIGHT = get_white(LightKelvinConstant.CLOUDY_DAYLIGHT)
WHITE_BLUE_DAYLIGHT = get_white(LightKelvinConstant.BLUE_DAYLIGHT)
WHITE_BLUE_OVERCAST = get_white(LightKelvinConstant.BLUE_OVERCAST)
WHITE_BLUE_WATER = get_white(LightKelvinConstant.BLUE_WATER)
WHITE_BLUE_ICE = get_white(LightKelvinConstant.BLUE_ICE)

WHITES_IN_KELVIN_CYCLE = [
    WHITE_ULTRA_WARM,
    WHITE_NEUTRAL,
    WHITE_DAYLIGHT,
    WHITE_BLUE_DAYLIGHT,
    WHITE_BLUE_ICE,
]

WHITE_START_INDEX = 2

ALL_WHITES = [
    WHITE_ULTRA_WARM,
    WHITE_INCANDESCENT,
    WHITE_WARM,
    WHITE_NEUTRAL_WARM,
    WHITE_NEUTRAL,
    WHITE_COOL,
    WHITE_COOL_DAYLIGHT,
    WHITE_SOFT_DAYLIGHT,
    WHITE_DAYLIGHT,
    WHITE_NOON_DAYLIGHT,
    WHITE_BRIGHT_DAYLIGHT,
    WHITE_CLOUDY_DAYLIGHT,
    WHITE_BLUE_DAYLIGHT,
    WHITE_BLUE_OVERCAST,
    WHITE_BLUE_WATER,
    WHITE_BLUE_ICE
]

# endregion

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
