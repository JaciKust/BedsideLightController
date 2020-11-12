class Toggleable:
    _is_on = False

    def _execute_set_on(self):
        pass

    def _execute_set_off(self):
        pass

    def set_on(self):
        try:
            self._execute_set_on()
            self._is_on = True
        except:
            pass

    def set_off(self):
        try:
            self._execute_set_off()
            self._is_on = False
        except:
            pass

    def toggle(self):
        if self._is_on:
            self.set_off()
        else:
            self.set_on()

    def get_is_on(self):
        return self._is_on
