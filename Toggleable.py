from Constants import DatabaseState
from Sql.MarraQueryMaker import MarraQueryMaker


class Toggleable:
    def __init__(self, database_id):
        self.database_id = database_id
        self.maker = MarraQueryMaker()
        self.maker.open_connection()

    _is_on = False

    def __del__(self):
        self.maker.close_connection()

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
        else:
            self._update_database(DatabaseState.ON)

    def set_off(self):
        try:
            self._execute_set_off()
            self._is_on = False
        except:
            pass
        else:
            self._update_database(DatabaseState.OFF)

    def toggle(self):
        if self._is_on:
            self.set_off()
        else:
            self.set_on()

    def get_is_on(self):
        return self._is_on

    def _update_database(self, status):
        try:
            self.maker.insert_toggleable_state(self.database_id, status)
        except:
            print("Unable to update database state for " + str(self.database_id))
            pass
