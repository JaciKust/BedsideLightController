from Interactable.Toggleable import Toggleable


class RemoteRelay(Toggleable):
    def __init__(self, database_id, pin):
        super().__init__(database_id)
        self.pin = pin

    send = None
    pulse = None

    def _execute_set_off(self):
        if self.send is None:
            return
        self.send(self.pin, 0)

    def _execute_set_on(self):
        if self.send is None:
            return
        self.send(self.pin, 1)

    def pulse_on_off(self):
        if self.pulse is None:
            return
        self.pulse(self.pin)
