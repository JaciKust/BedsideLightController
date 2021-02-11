from Interactable.Light.LifxLamp import LifxLamp
from Interactable.Light.LifxLight import LifxLight

alpha = LifxLight('d0:73:d5:2b:5b:08', '192.168.0.200', 'Alpha')
foxtrot = LifxLight('D0:73:D5:40:15:4C', '192.168.0.205', 'Foxtrot')
echo = LifxLight('D0:73:D5:40:31:1D', '192.168.0.204', 'Echo')

# Yellow Lamp
bravo = LifxLight('d0:73:d5:2a:69:0c', '192.168.0.201', 'Bravo')
charlie = LifxLight('D0:73:D5:2B:BA:14', '192.168.0.202', 'Charlie')
delta = LifxLight('D0:73:D5:2B:96:41', '192.168.0.203', 'Delta')

# Silver
golf = LifxLight('D0:73:D5:2A:93:0C', '192.168.0.206', 'Golf')

# White bedside
hotel = LifxLight('D0:73:D5:2B:F7:AB', '192.168.0.207', 'Hotel')

# Black bedside
india = LifxLight('D0:73:D5:2C:09:DD', '192.168.0.208', 'India')

all_lights = [
    alpha,
    bravo,
    charlie,
    delta,
    echo,
    foxtrot,
    golf,
    hotel,
    india,
]

black_bedside_lamp = [
    india
]

white_bedside_lamp = [
    hotel
]

red_lights = [
    alpha,
    foxtrot,
    echo
]

yellow_lights = [
    bravo,
    charlie,
    delta
]

bedside_lamps = white_bedside_lamp + black_bedside_lamp
desk_lamps = yellow_lights + red_lights

silver_lamp = [
    golf
]

red_lamp = LifxLamp(red_lights, "Red")
yellow_lamp = LifxLamp(yellow_lights, "Yellow")
entry_lamp = LifxLamp(silver_lamp, "Entry")
jaci_bedside_lamp = LifxLamp(bedside_lamps, "BedSide")
all_lamp = LifxLamp(all_lights, "All")
desk_lamp = LifxLamp(desk_lamps, "Desk")
bed_black_lamp = LifxLamp(black_bedside_lamp, "Black")
bed_white_lamp = LifxLamp(white_bedside_lamp, "White")
