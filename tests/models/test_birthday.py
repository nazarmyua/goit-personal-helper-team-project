import unittest
from datetime import datetime

from src.constants.constants import DATE_FORMAT
from src.models.birthday import Birthday


class TestBirthday(unittest.TestCase):
    def test_error_parsing1(self):
        with self.assertRaises(ValueError):
            Birthday("31.06.1993")

    def test_error_parsing2(self):
        with self.assertRaises(ValueError):
            Birthday("30.06.19931")

    def test_parsing_valid(self):
        birthday_str = datetime.now().strftime(DATE_FORMAT)
        birthday = Birthday(birthday_str)
        self.assertEqual(birthday_str, f"{birthday}")


if __name__ == "__main__":
    unittest.main()
