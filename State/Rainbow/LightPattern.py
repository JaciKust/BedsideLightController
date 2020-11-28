from Constants import Light as LightConstant
from Constants import Rainbow


class LightPattern:
    def __init__(self, lights, colors, name, all_pattern=False):
        assert all_pattern or len(lights) == len(colors), \
            "Length of lights must equal length of colors {} != {}".format(len(lights), len(colors))
        self.all_pattern = all_pattern
        self.lights = lights
        self.colors = colors
        self.name = name


primary_cycle_three = LightPattern(Rainbow.three_lights, Rainbow.primary_color_3, "Primary Cycle 3")
# secondary_cycle_three = LightPattern(Rainbow.three_lights, Rainbow.secondary_colors_3, "Secondary Cycle 3")
rainbow_all = LightPattern(Rainbow.all_lights, Rainbow.rainbow_5, "Rainbow All")
bright = LightPattern(Rainbow.three_lights, Rainbow.bright_3, "Bright")
shadows = LightPattern(Rainbow.three_lights, Rainbow.shadows_3, "Shadows")
blue_cycle = LightPattern(Rainbow.three_lights, Rainbow.blue_cycle_3, "Blue Cycle")
cyan_cycle = LightPattern(Rainbow.all_lights, Rainbow.cyan_cycle_5, "Cyan Cycle")
rainbow_one = LightPattern(LightConstant.all_lights, Rainbow.all_six, "One Cycle", True)
primary_one = LightPattern(LightConstant.all_lights, Rainbow.primary_color_3, "One Primary", True)

patterns = [
    primary_cycle_three,
    primary_one,
    rainbow_one,
    rainbow_all,
    cyan_cycle,
    bright,
    shadows,
    blue_cycle
]
