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


DIM = 20
DARK = 1
FULL = 100
OFF = 0

RED = Color(FULL, OFF, OFF)
GREEN = Color(OFF, FULL, OFF)
BLUE = Color(OFF, OFF, FULL)

DIM_RED = Color(DIM, OFF, OFF)
DIM_GREEN = Color(OFF, DIM, OFF)
DIM_BLUE = Color(OFF, OFF, DIM)

DARK_RED = Color(DARK, OFF, OFF)
DARK_GREEN = Color(OFF, DARK, OFF)
DARK_BLUE = Color(OFF, OFF, DARK)

CYAN = Color(OFF, FULL, FULL)
MAGENTA = Color(FULL, OFF, FULL)
YELLOW = Color(FULL, FULL, OFF)

DIM_CYAN = Color(OFF, DIM, DIM)
DIM_MAGENTA = Color(DIM, OFF, DIM)
DIM_YELLOW = Color(DIM, DIM, OFF)

DARK_CYAN = Color(OFF, DARK, DARK)
DARK_MAGENTA = Color(DARK, OFF, DARK)
DARK_YELLOW = Color(DARK, DARK, OFF)

DARK_WHITE = Color(DARK, DARK, DARK)
DIM_WHITE = Color(DIM, DIM, DIM)
BLACK = Color(OFF, OFF, OFF)

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
