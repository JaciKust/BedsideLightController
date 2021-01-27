from lifxlan import Light, Group

# Red Lamp
alpha = Light('d0:73:d5:2b:5b:08', '192.168.0.200')
foxtrot = Light('D0:73:D5:40:15:4C', '192.168.0.205')
echo = Light('D0:73:D5:40:31:1D', '192.168.0.204')

# Yellow Lamp
bravo = Light('d0:73:d5:2a:69:0c', '192.168.0.201')
charlie = Light('D0:73:D5:2B:BA:14', '192.168.0.202')
delta = Light('D0:73:D5:2B:96:41', '192.168.0.203')

# Silver
golf = Light('D0:73:D5:2A:93:0C', '192.168.0.206')

# White bedside
hotel = Light('D0:73:D5:2B:F7:AB', '192.168.0.207')

# Black bedside
india = Light('D0:73:D5:2C:09:DD', '192.168.0.208')

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

red_lamp = [
    alpha,
    foxtrot,
    echo
]

yellow_lamp = [
    bravo,
    charlie,
    delta
]

bedside_lamps = white_bedside_lamp + black_bedside_lamp
desk_lamps = yellow_lamp + red_lamp

silver_lamp = [
    golf
]

red_group = Group(red_lamp)
yellow_group = Group(yellow_lamp)
entry_group = Group(silver_lamp)
jaci_bedside_group = Group(bedside_lamps)
all_group = Group(all_lights)
desk_group = Group(desk_lamps)
bed_black_group = Group(black_bedside_lamp)
bed_white_group = Group(white_bedside_lamp)
