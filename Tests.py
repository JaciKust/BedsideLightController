import unittest

from AsleepLightsOnState import AsleepLightsOnState
from AsleepLightsOffState import AsleepLightsOffState


class MyTestCase(unittest.TestCase):
    def test_something(self):
        self.assertEqual(True, False)


class TestStateEquality(unittest.TestCase):
    def test_same_state_equal(self):
        asleepLighsOff = AsleepLightsOffState(None)
        asleepLightsOffTwo = AsleepLightsOffState(None)
        self.assertEqual(asleepLighsOff, asleepLightsOffTwo)

    def test_different_state_not_equal(self):
        asleepLightsOff = AsleepLightsOffState(None)
        asleepLightsOn = AsleepLightsOnState(None)
        self.assertNotEqual(asleepLightsOff, asleepLightsOn)


if __name__ == '__main__':
    unittest.main()
