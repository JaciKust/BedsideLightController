import unittest
from datetime import datetime, timedelta

from Interactable.TimeStampedState import TimeStampedState
from Interactable.ToggleableOnTimeCalculator import ToggleableOnTimeCalculator

time_10 = datetime(2020, 1, 1, 10)
time_11 = datetime(2020, 1, 1, 11)
time_12 = datetime(2020, 1, 1, 12)
time_13 = datetime(2020, 1, 1, 13)
time_14 = datetime(2020, 1, 1, 14)
time_15 = datetime(2020, 1, 1, 15)
time_16 = datetime(2020, 1, 1, 16)
time_17 = datetime(2020, 1, 1, 17)


class MyTestCase(unittest.TestCase):

    def test_one_range(self):
        start = TimeStampedState(time_10, True)
        end = TimeStampedState(time_11, False)

        expected = timedelta(hours=1)

        result = ToggleableOnTimeCalculator.get_on_time([start, end], True, time_11)
        self.assertEqual(expected, result)

    def test_two_ranges(self):
        start_1 = TimeStampedState(time_10, True)
        end_1 = TimeStampedState(time_11, False)

        start_2 = TimeStampedState(time_12, True)
        end_2 = TimeStampedState(time_13, False)

        dataset = [start_1, end_1, start_2, end_2]
        expected = timedelta(hours=2)

        result = ToggleableOnTimeCalculator.get_on_time(dataset, True, time_11)
        self.assertEqual(expected, result)

    def test_two_on_in_a_row(self):
        start_1 = TimeStampedState(time_10, True)
        start_2 = TimeStampedState(time_11, True)
        end_1 = TimeStampedState(time_12, False)

        dataset = [start_1, start_2, end_1]
        expected = timedelta(hours=2)

        result = ToggleableOnTimeCalculator.get_on_time(dataset, True, time_12)
        self.assertEqual(expected, result)

    def test_leave_on(self):
        start_1 = TimeStampedState(time_10, True)
        end_1 = TimeStampedState(time_12, False)

        start_2 = TimeStampedState(time_14, True)
        now = time_16

        dataset = [start_1, end_1, start_2]
        expected = timedelta(hours=4)

        result = ToggleableOnTimeCalculator.get_on_time(dataset, True, now)
        self.assertEqual(expected, result)

    def test_start_false(self):
        begin = TimeStampedState(time_10, False)

        start_1 = TimeStampedState(time_11, True)
        end_1 = TimeStampedState(time_12, False)

        dataset = [begin, start_1, end_1]
        expected = timedelta(hours=1)

        result = ToggleableOnTimeCalculator.get_on_time(dataset, True, time_13)
        self.assertEqual(expected, result)

    def test_end_on_but_on_is_now(self):
        start_1 = TimeStampedState(time_11, True)
        end_1 = TimeStampedState(time_12, False)

        start_2 = TimeStampedState(time_13, True)

        dataset = [start_1, end_1, start_2]
        expected = timedelta(hours=1)
        now = time_13

        result = ToggleableOnTimeCalculator.get_on_time(dataset, True, now)
        self.assertEqual(expected, result)

    def test_for_not_true(self):
        start = TimeStampedState(time_10, 'hello')
        end = TimeStampedState(time_11, 'world')

        expected = timedelta(hours=1)

        result = ToggleableOnTimeCalculator.get_on_time([start, end], 'hello', time_11)
        self.assertEqual(expected, result)

    def test_for_not_true_complex(self):
        look_for_state = 'hello'

        start_1 = TimeStampedState(time_10, look_for_state)
        end_1 = TimeStampedState(time_11, 'world')
        other = TimeStampedState(time_12, 'hi')
        another = TimeStampedState(time_13, 'mars')
        start_2 = TimeStampedState(time_14, look_for_state)
        start_3 = TimeStampedState(time_15, look_for_state)
        end_2 = TimeStampedState(time_16, 'saturn')

        dataset = [start_1, end_1, other, another, start_2, start_3, end_2]
        expected = timedelta(hours=3)

        result = ToggleableOnTimeCalculator.get_on_time(dataset, look_for_state, time_17)
        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()
