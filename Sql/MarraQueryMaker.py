import os
import sys

import psycopg2 as psycopg2

from Sql import MarraQuery

sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'Common'))
import MarraDatabaseConfig

class MarraQueryMaker:
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if MarraQueryMaker.__instance == None:
            MarraQueryMaker()
        return MarraQueryMaker.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MarraQueryMaker.__instance != None:
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

        self.connection = psycopg2.connect(
            dbname=self.marra_database_name,
            host=self.marra_database_host,
            user=self.marra_database_user,
            password=self.marra_database_pass
        )

        self.connection.autocommit = True

    def close_connection(self):
        try:
            if self.connection is not None:
                self.connection.close()
                self.connection = None
        except:
            pass

    def insert_toggleable_state(self, toggleable_id, state):
        cursor = self.connection.cursor()
        cursor.execute(MarraQuery.insert_state_update, (toggleable_id, state))
        cursor.close()

    def insert_state_status(self, state_id):
        cursor = self.connection.cursor()
        cursor.execute(MarraQuery.insert_state_status, (state_id,))

