class RemoteRelayState:
    def __init__(self, pin, state):
        self.name = 'RelayState'
        self.pin = pin
        self.state = state
