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

# Bedside Door
hotel = Light('D0:73:D5:2B:F7:AB', '192.168.0.207')

# Bedside Wall
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

window_lights = [
    alpha,
    bravo,
]

room_lights = [
    charlie,
    delta,
    echo,
    foxtrot,
    golf,
    hotel,
    india
]

desk_lights = [
    hotel,
    india
]

general_lights = [
    charlie,
    delta,
    echo,
    foxtrot,
    golf
]

window_group = Group(window_lights)
room_group = Group(room_lights)
all_group = Group(all_lights)

pidgey_lamp = [
    india
]

oddish_lamp = [
    hotel
]

# -------------------------------------------
jaci_bedside = [
    india,
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

silver_lamp = [
    golf
]

computer_lamps = silver_lamp + yellow_lamp
