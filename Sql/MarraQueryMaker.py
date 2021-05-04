import os
import sys

import psycopg2 as psycopg2

from Interactable.TimeStampedState import TimeStampedState
from Sql import MarraQuery

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Common'))
import MarraDatabaseConfig
import logging

class MarraQueryMaker:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MarraQueryMaker.__instance is None:
            MarraQueryMaker()
        return MarraQueryMaker.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MarraQueryMaker.__instance is not None:
            raise Exception("This class is a singleton!")
        else:
            self.marra_database_host = MarraDatabaseConfig.postgres['host']
            self.marra_database_name = MarraDatabaseConfig.postgres['name']
            self.marra_database_user = MarraDatabaseConfig.postgres['username']
            self.marra_database_pass = MarraDatabaseConfig.postgres['password']
            self.connection = None

            MarraQueryMaker.__instance = self

    def __del__(self):
        self.close_connection()

    def open_connection(self):
        if self.connection is not None:
            return
        try:
            self.connection = psycopg2.connect(
                dbname=self.marra_database_name,
                host=self.marra_database_host,
                user=self.marra_database_user,
                password=self.marra_database_pass
            )
            self.connection.autocommit = True
        except:
            logging.warning("Could not connect to Marra.")
            self.close_connection()

    def close_connection(self):
        try:
            if self.connection is not None:
                self.connection.close()
        except:
            pass
        finally:
            self.connection = None

    def insert_toggleable_state(self, toggleable_id, state):
        if self.connection is None:
            self.open_connection()

        try:
            bit_state = self._to_bit(state)
            cursor = self.connection.cursor()
            cursor.execute(MarraQuery.insert_state_update, (toggleable_id, bit_state))
            # cursor.close()
        except Exception as e:
            logging.warning("Could not write toggleable state to Marra.")
            self.close_connection()

    def insert_state_status(self, state_id):
        if self.connection is None:
            self.open_connection()

        try:
            cursor = self.connection.cursor()
            cursor.execute(MarraQuery.insert_state_status, (state_id,))
        except:
            logging.warning("Could not write state to Marra.")
            self.close_connection()

    def get_time_stamps_for_toggleable_state_change_today(self, toggleable_id):
        if self.connection is None:
            self.open_connection()

        cursor = self.connection.cursor()
        try:
            cursor.execute(MarraQuery.get_time_stamps_for_toggleable_state_change_today, (toggleable_id,))

            table = cursor.fetchall()
            stamped_states = []
            for data_row in table:
                stamped_states.append(TimeStampedState.from_toggleable_state_change(data_row))

            return stamped_states
        except Exception as e:
            logging.warning("Could not get toggleable states for today from Marra.")
            self.close_connection()

    def get_latest_toggleable_state_for_yesterday(self, toggleable_id):
        if self.connection is None:
            self.open_connection()

        cursor = self.connection.cursor()
        try:
            cursor.execute(MarraQuery.get_last_time_stamp_for_toggleabale_state_change, (toggleable_id,))

            data_row = cursor.fetchone()
            return TimeStampedState.from_toggleable_state_change(data_row)
        except Exception as e:
            logging.warning("Could not get yesterday's states.")
            self.close_connection()

    def _to_bit(self, theInt):
        return theInt == 1
