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


class TestSearchNotes(unittest.TestCase):
    def setUp(self):
        self.address_book = AddressBook()

        # First record
        self.record1 = Record("John")
        self.record1.add_note("Buy milk")
        self.record1.add_note("Call mom")
        self.address_book.add_record(self.record1)

        # Second record
        self.record2 = Record("Mike")
        self.record2.add_note("Work meeting at 5 PM")
        self.record2.add_note("Milk delivery tomorrow")
        self.address_book.add_record(self.record2)

        # Third record (no notes)
        self.record3 = Record("Sarah")
        self.address_book.add_record(self.record3)

    def test_find_single_match(self):
        """Keyword matches a single note in a single record."""
        result = self.address_book.get_records_by_note_keyword("call")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].name.value, "John")
        self.assertEqual(len(result[0].notes), 1)  # filtered notes
        self.assertIn("call", next(iter(result[0].notes.values())).value.lower())

    def test_find_multiple_matches_in_one_record(self):
        """Keyword matches multiple notes in one record."""
        result = self.address_book.get_records_by_note_keyword("milk")
        self.assertEqual(len(result), 2)

        names = {r.name.value for r in result}
        self.assertIn("John", names)
        self.assertIn("Mike", names)

    def test_find_note_case_insensitive(self):
        result = self.address_book.get_records_by_note_keyword("MiLk")
        self.assertEqual(len(result), 2)

    def test_find_no_matches(self):
        result = self.address_book.get_records_by_note_keyword("unicorn")
        self.assertEqual(len(result), 0)

    def test_find_keyword_with_whitespace_trim(self):
        result = self.address_book.get_records_by_note_keyword("   milk   ")
        self.assertEqual(len(result), 2)

    def test_empty_keyword_returns_empty_list(self):
        result = self.address_book.get_records_by_note_keyword("")
        self.assertEqual(len(result), 0)

        result = self.address_book.get_records_by_note_keyword("   ")
        self.assertEqual(len(result), 0)

    def test_record_without_notes_is_skipped(self):
        """Sarah has no notes — should not appear in any result."""
        result = self.address_book.get_records_by_note_keyword("milk")
        names = {r.name.value for r in result}
        self.assertNotIn("Sarah", names)

    def test_only_filtered_notes_returned(self):
        """Returned Record must contain ONLY notes that matched."""
        result = self.address_book.get_records_by_note_keyword("mom")
        self.assertEqual(len(result), 1)
        john = result[0]

        self.assertEqual(john.name.value, "John")
        self.assertEqual(len(john.notes), 1)
        self.assertEqual(list(john.notes.values())[0].value, "Call mom")


if __name__ == "__main__":
    unittest.main()
