import datetime
import unittest

import TimeFunctions


class MyTestCase(unittest.TestCase):
    def test_next_five_on_next_day(self):
        search_for_time = datetime.time(5, 0)
        result = TimeFunctions.get_next(search_for_time, datetime.datetime(2009, 12, 6, 10, 0))
        expected = datetime.datetime(2009, 12, 7, 5, 0)
        self.assertEqual(expected, result)

    def test_next_five_on_today(self):
        search_for_time = datetime.time(5, 0)
        result = TimeFunctions.get_next(search_for_time, datetime.datetime(2009, 12, 6, 4, 0))
        expected = datetime.datetime(2009, 12, 6, 5, 0)
        self.assertEqual(expected, result)

    def test_next_five_in_one_minute_today(self):
        search_for_time = datetime.time(5, 0)
        result = TimeFunctions.get_next(search_for_time, datetime.datetime(2009, 12, 6, 4, 59))
        expected = datetime.datetime(2009, 12, 6, 5, 0)
        self.assertEqual(expected, result)

    def test_next_five_in_zero_minutes_today(self):
        search_for_time = datetime.time(5, 0)
        result = TimeFunctions.get_next(search_for_time, datetime.datetime(2009, 12, 6, 5, 0))
        expected = datetime.datetime(2009, 12, 7, 5, 0)
        self.assertEqual(expected, result)

    def test_next_five_one_minute_past(self):
        search_for_time = datetime.time(5, 0)
        result = TimeFunctions.get_next(search_for_time, datetime.datetime(2009, 12, 6, 5, 1))
        expected = datetime.datetime(2009, 12, 7, 5, 0)
        self.assertEqual(expected, result)

    def get_next_five_at_midnight(self):
        search_for_time = datetime.time(5, 0)
        result = TimeFunctions.get_next(search_for_time, datetime.datetime(2009, 12, 6, 0, 0))
        expected = datetime.datetime(2009, 12, 6, 5, 0)
        self.assertEqual(expected, result)


if __name__ == '__main__':
    unittest.main()
