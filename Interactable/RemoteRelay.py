from Interactable.Toggleable import Toggleable


class RemoteRelay(Toggleable):
    def __init__(self, database_id, pin):
        super().__init__(database_id)
        self.pin = pin

    send = None

    def _execute_set_off(self):
        self.send(self.pin, 0)

    def _execute_set_on(self):
        self.send(self.pin, 1)
