import logging
import threading
from datetime import timedelta, datetime

from Constants import DatabaseState
from Interactable.TimeStampedState import TimeStampedState
from Interactable.ToggleableOnTimeCalculator import ToggleableOnTimeCalculator
from Sql.MarraQueryMaker import MarraQueryMaker


class Toggleable:
    def __init__(self, database_id, max_time_on=None):
        self.database_id = database_id
        self.maker = MarraQueryMaker.getInstance()
        self.max_time_on = max_time_on

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
        else:
            thread = threading.Thread(target=self._update_database, args=(DatabaseState.ON,))
            thread.start()

    def set_off(self):
        try:
            self._execute_set_off()
            self._is_on = False
        except:
            pass
        else:
            thread = threading.Thread(target=self._update_database, args=(DatabaseState.OFF,))
            thread.start()

    def soft_set_on(self):
        if self.max_time_on is not None and self.get_time_in_toggleable_state() > self.max_time_on:
            return

        self.set_on()

    def set_off_if_over_max_time(self):
        if self.max_time_on is not None and self.get_time_in_toggleable_state() > self.max_time_on:
            self.set_off()

    def set_on_if_under_max_time(self):
        if self.max_time_on is not None and self.get_time_in_toggleable_state() < self.max_time_on:
            self.set_on()

    def toggle(self):
        if self._is_on:
            self.set_off()
        else:
            self.set_on()

    def get_time_in_toggleable_state(self):
        try:
            todays_entries = self.maker.get_time_stamps_for_toggleable_state_change_today(self.database_id)
            todays_start_state = self.maker.get_latest_toggleable_state_for_yesterday(self.database_id)

            if todays_start_state is not None:
                todays_start_state.time_stamp = datetime(
                    year=todays_start_state.time_stamp.year,
                    month=todays_start_state.time_stamp.month,
                    day=todays_start_state.time_stamp.day,
                    hour=0,
                    minute=0) \
                                                + timedelta(days=1)
                first = [todays_start_state]
                first.extend(todays_entries)
                times = first
            else:  # todays_start_state is None
                now = datetime.now()
                start = datetime(year=now.year, month=now.month, day=now.day, hour=0)

                if len(todays_entries) > 0:
                    first_state = todays_entries[0]

                    first = [TimeStampedState(start, first_state)]
                    first.extend(todays_entries)

                    times = first
                else:
                    times = TimeStampedState(start, self._is_on)
            return ToggleableOnTimeCalculator.get_on_time(times, True)

        except Exception as e:
            logging.warning("Could not get data about a toggleable from Marra")
        finally:
            pass

    def get_is_on(self):
        return self._is_on

    def write_current_state_to_database(self):
        if (self._is_on):
            state = DatabaseState.ON
        else:
            state = DatabaseState.OFF

        self._update_database(state)

    def _update_database(self, status):

        try:
            self.maker.insert_toggleable_state(self.database_id, status)
        except:
            print("Unable to update database state for " + str(self.database_id))
            pass
        finally:
            pass
            # self.maker.close_connection()
