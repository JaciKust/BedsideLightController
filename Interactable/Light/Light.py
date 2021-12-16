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

# Light Bar
juliet = LifxLight('D0:73:D5:59:E4:BE', '192.168.0.209', 'Juliet')
kilo = LifxLight('D0:73:D5:57:A1:C7', '192.168.0.210', 'Kilo')

lima = LifxLight('D0:73:D5:51:FF:5C', '192.168.0.211', 'Lima')
mike = LifxLight('D0:73:D5:3E:73:4C', '192.168.0.212', 'Mike')

# Ledge Lights
november = LifxLight('D0:73:D5:65:10:44', '192.168.0.213', 'November')
oscar = LifxLight('D0:73:D5:65:72:EE', '192.168.0.214', 'Oscar')

# Window Lights
papa = LifxLight('D0:73:D5:64:96:20', '192.168.0.215', 'Papa')
quebec = LifxLight('D0:73:D5:65:54:5C', '192.168.0.216', 'Quebec')

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
    juliet,
    kilo,
    lima,
    mike,
    november,
    oscar,
    papa,
    quebec
]
black_bar_lamp = [
    juliet,
    kilo
]

white_bar_lamp = [
    lima,
    mike
]

bar_lamp = black_bar_lamp + white_bar_lamp

black_bedside_lamp = [
    india
]

white_bedside_lamp = [
    hotel
]

black_side = black_bar_lamp + black_bedside_lamp
white_side = white_bar_lamp + white_bedside_lamp

window_lights = [
    papa,
    quebec
]

ledge_lights = [
    november,
    oscar
]

red_lights = [
    alpha,
    foxtrot,
    echo
]

big_red_lights = red_lights + ledge_lights
huge_red_lights = big_red_lights + window_lights

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

red_lamp = LifxLamp(red_lights, 'Red')
yellow_lamp = LifxLamp(yellow_lights, 'Yellow')
entry_lamp = LifxLamp(silver_lamp, 'Entry')
jaci_bedside_lamp = LifxLamp(bedside_lamps, 'BedSide')
all_lamp = LifxLamp(all_lights, 'All')
desk_lamp = LifxLamp(desk_lamps, 'Desk')
bed_black_lamp = LifxLamp(black_bedside_lamp, 'Black')
bed_white_lamp = LifxLamp(white_bedside_lamp, 'White')
black_side = LifxLamp(black_side, 'Black Side')
white_side = LifxLamp(white_side, 'White Side')
ledge_lamp = LifxLamp(ledge_lights, 'Ledge')
window_lamp = LifxLamp(window_lights, 'Windows')

big_red_lamp = LifxLamp(big_red_lights, "Big Red")
huge_red_lamp = LifxLamp(huge_red_lights, "Huge Red")
