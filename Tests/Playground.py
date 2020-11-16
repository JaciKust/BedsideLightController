import unittest

from Sql.MarraQueryMaker import MarraQueryMaker


class MyTestCase(unittest.TestCase):
    def test_something(self):
        try:
            maker = MarraQueryMaker()
            maker.open_connection()
            maker.insert_toggleable_state(1, 0)
        finally:
            del maker
        self.assertTrue(True)


if __name__ == '__main__':
    unittest.main()
