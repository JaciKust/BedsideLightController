from lifxlan import Light, Group

alpha = Light('d0:73:d5:2b:5b:08', '192.168.0.200')
beta = Light('d0:73:d5:2a:69:0c', '192.168.0.201')
charlie = Light('D0:73:D5:2B:BA:14', '192.168.0.202')
delta = Light('D0:73:D5:2B:96:41', '192.168.0.203')
echo = Light('D0:73:D5:40:31:1D', '192.168.0.204')
foxtrot = Light('D0:73:D5:40:15:4C', '192.168.0.205')
gamma = Light('D0:73:D5:2A:93:0C', '192.168.0.206')
hotel = Light('D0:73:D5:2B:F7:AB', '192.168.0.207')
india = Light('D0:73:D5:2C:09:DD', '192.168.0.208')

all_lights = [
    alpha,
    beta,
    charlie,
    delta,
    echo,
    foxtrot,
    gamma,
    hotel,
    india,
]

window_lights = [
    alpha,
    beta,
]

room_lights = [
    charlie,
    delta,
    echo,
    foxtrot,
    gamma,
    hotel,
    india
]

window_group = Group(window_lights)
room_group = Group(room_lights)
all_group = Group(all_lights)

