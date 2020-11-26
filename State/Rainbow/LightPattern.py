from Constants import Rainbow


class LightPattern:
    def __init__(self, lights, colors, name):
        assert len(lights) == len(colors), \
            "Length of lights must equal length of colors {} != {}".format(len(lights), len(colors))
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

patterns = [
    primary_cycle_three,
    rainbow_all,
    bright,
    shadows,
    blue_cycle,
    cyan_cycle
]
