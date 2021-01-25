from Constants import Light as LightConstant
from Constants import Rainbow
from State.Rainbow import PatternType


class BaseLightPattern:
    def __init__(self, lights, colors, name, pattern):
        assert pattern != PatternType.BASE or len(lights) == len(colors), \
            "Length of lights must equal length of colors {} != {}".format(len(lights), len(colors))
        self.pattern = pattern
        self.lights = lights
        self.colors = colors
        self.name = name


primary_cycle_three = BaseLightPattern(Rainbow.three_lights, Rainbow.primary_color_3, "Primary Cycle 3",
                                       PatternType.BASE)
rainbow_all = BaseLightPattern(Rainbow.all_lights, Rainbow.rainbow_5, "Rainbow All", PatternType.BASE)
bright = BaseLightPattern(Rainbow.three_lights, Rainbow.bright_3, "Bright", PatternType.BASE)
shadows = BaseLightPattern(Rainbow.three_lights, Rainbow.shadows_3, "Shadows", PatternType.BASE)
blue_cycle = BaseLightPattern(Rainbow.three_lights, Rainbow.blue_cycle_3, "Blue Cycle", PatternType.BASE)
cyan_cycle = BaseLightPattern(Rainbow.all_lights, Rainbow.cyan_cycle_5, "Cyan Cycle", PatternType.BASE)

rainbow_one = BaseLightPattern(LightConstant.all_lights, Rainbow.all_six, "One Cycle", PatternType.ONE)
primary_one = BaseLightPattern(LightConstant.all_lights, Rainbow.primary_color_3, "One Primary", PatternType.ONE)

primary_random = BaseLightPattern(Rainbow.three_lights, Rainbow.primary_color_3, "Random Primary Cycle 3",
                                  PatternType.RANDOM)
all_random = BaseLightPattern(Rainbow.most_lights, Rainbow.all_six, "Random All Cycle 3", PatternType.RANDOM)
patterns = [
    all_random,
    primary_cycle_three,
    primary_one,
    primary_random,
    rainbow_one,
    rainbow_all,
    cyan_cycle,
    bright,
    shadows,
    blue_cycle
]
