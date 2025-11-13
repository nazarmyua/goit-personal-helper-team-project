import unittest
from datetime import datetime, timedelta

from src.constants import DATE_FORMAT
from src.models import AddressBook
from src.models.record import Record


class TestBirthday(unittest.TestCase):
    def init_address_book(self):
        self.address_book = AddressBook()

    def test_add_record(self):
        self.init_address_book()
        record = Record("Mike")
        record.add_phone("1234567890")
        self.address_book.add_record(record)
        self.assertEqual(len(self.address_book) == 1, True)

    def test_find_record(self):
        self.init_address_book()
        record = Record("Mike")
        record.add_phone("1234567890")
        self.address_book.add_record(record)

        mike_record = self.address_book.find("Mike")
        self.assertEqual(mike_record, record)

    def test_remove_record(self):
        self.init_address_book()
        record = Record("Mike")
        record.add_phone("1234567890")
        self.address_book.add_record(record)
        self.assertEqual(len(self.address_book) == 1, True)

        self.address_book.delete("Mike")
        self.assertEqual(len(self.address_book) == 0, True)

    def test_get_upcoming_birthdays(self):
        self.init_address_book()
        record = Record("Mike")
        record.add_phone("1234567890")
        tomorrow = datetime.now() + timedelta(days=1)
        birthday_str = tomorrow.strftime(DATE_FORMAT)
        record.add_birthday(birthday_str)

        self.address_book.add_record(record)

        birthdays = self.address_book.get_upcoming_birthdays()
        assert len(birthdays) == 1


if __name__ == "__main__":
    unittest.main()
