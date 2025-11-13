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

        found_records = self.address_book.search("Mike")
        self.assertEqual(len(found_records), 1)

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

    def test_find_many_records(self):
        self.init_address_book()
        record = Record("Mike Wazowski")
        record.add_phone("1234567890")
        tomorrow = datetime.now() + timedelta(days=1)
        birthday_str = tomorrow.strftime(DATE_FORMAT)
        record.add_birthday(birthday_str)

        self.address_book.add_record(record)

        record = Record("Dwight Shchrute")
        record.add_phone("3213213211")
        tomorrow = datetime.now() + timedelta(days=2)
        birthday_str = tomorrow.strftime(DATE_FORMAT)
        record.add_birthday(birthday_str)

        self.address_book.add_record(record)

        found_records = self.address_book.search("3")
        self.assertEqual(len(found_records), 2)

        found_records = self.address_book.search("i")
        self.assertEqual(len(found_records), 2)

        found_records = self.address_book.search("Dwi")
        self.assertEqual(len(found_records), 1)

        found_records = self.address_book.search("Mike")
        self.assertEqual(len(found_records), 1)

        found_records = self.address_book.search("Mike Wazowski")
        self.assertEqual(len(found_records), 1)

        found_records = self.address_book.search("Wazowski")
        self.assertEqual(len(found_records), 1)

        found_records = self.address_book.search("Mikelo")
        self.assertEqual(len(found_records), 0)

        found_records = self.address_book.search("")
        self.assertEqual(len(found_records), 0)


if __name__ == "__main__":
    unittest.main()
