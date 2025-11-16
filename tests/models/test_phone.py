import unittest

from src.models.record import Record
from src.models.phone import Phone


class TestPhone(unittest.TestCase):
    # VALID CASES

    def test_valid_ukrainian_local_10_digits(self):
        phone = Phone("0954325444")
        self.assertEqual(phone.value, "0954325444")
        self.assertEqual(str(phone), "0954325444")

    def test_valid_international_with_plus(self):
        phone = Phone("+180943223757")
        self.assertEqual(phone.value, "180943223757")

    def test_valid_international_without_plus(self):
        phone = Phone("180943223757")
        self.assertEqual(phone.value, "180943223757")

    def test_valid_with_spaces_and_dashes(self):
        phone = Phone("+1 809 432-3757")
        self.assertEqual(phone.value, "18094323757")

    def test_valid_with_dots_and_parentheses(self):
        phone = Phone("(095) 432.54.44")
        self.assertEqual(phone.value, "0954325444")

    # INVALID CASES

    def test_phone_must_be_string(self):
        with self.assertRaises(ValueError) as ctx:
            Phone(1234567890)
        self.assertEqual(str(ctx.exception), "Phone number must be a string")

    def test_phone_cannot_be_empty(self):
        with self.assertRaises(ValueError) as ctx:
            Phone("")
        self.assertEqual(str(ctx.exception), "Phone number cannot be empty")

    def test_phone_cannot_be_whitespace_only(self):
        with self.assertRaises(ValueError) as ctx:
            Phone("   ")
        self.assertEqual(str(ctx.exception), "Phone number cannot be empty")

    def test_invalid_format_too_short(self):
        with self.assertRaises(ValueError) as ctx:
            Phone("123456789")
        self.assertEqual(str(ctx.exception), "Invalid phone number format")

    def test_invalid_format_non_digit_characters(self):
        with self.assertRaises(ValueError) as ctx:
            Phone("09543x5444")
        self.assertEqual(str(ctx.exception), "Invalid phone number format")

    def test_invalid_format_only_symbols(self):
        with self.assertRaises(ValueError) as ctx:
            Phone("+-()")
        self.assertEqual(str(ctx.exception), "Invalid phone number format")

    def test_invalid_format_too_many_digits(self):
        with self.assertRaises(ValueError) as ctx:
            Phone("+1234567890123456")
        self.assertEqual(str(ctx.exception), "Invalid phone number format")


class TestAddPhone(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")

    def test_add_single_phone(self):
        self.record.add_phone("1234567890")
        self.assertEqual(len(self.record.phones), 1)
        self.assertEqual(self.record.phones[0].value, "1234567890")

    def test_add_multiple_phones(self):
        self.record.add_phone("1234567890")
        self.record.add_phone("9876543210")
        self.assertEqual(len(self.record.phones), 2)

    def test_add_duplicate_phone_not_added(self):
        self.record.add_phone("1234567890")
        self.record.add_phone("1234567890")
        self.assertEqual(len(self.record.phones), 1)

    def test_add_phone_with_special_characters_filtered(self):
        self.record.add_phone("(123) 456-7890")
        self.assertEqual(self.record.phones[0].value, "1234567890")

    def test_add_phone_invalid_raises(self):
        with self.assertRaises(ValueError):
            self.record.add_phone("abc")


class TestRemovePhone(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")
        self.record.add_phone("1234567890")
        self.record.add_phone("9876543210")

    def test_remove_phone_success(self):
        self.record.remove_phone("1234567890")
        self.assertEqual(len(self.record.phones), 1)
        self.assertEqual(self.record.phones[0].value, "9876543210")

    def test_remove_phone_not_found_silent(self):
        self.record.remove_phone("5555555555")
        self.assertEqual(len(self.record.phones), 2)

    def test_remove_all_phones(self):
        self.record.remove_phone("1234567890")
        self.record.remove_phone("9876543210")
        self.assertEqual(len(self.record.phones), 0)


class TestEditPhone(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")
        self.record.add_phone("1234567890")
        self.record.add_phone("9876543210")

    def test_edit_phone_success(self):
        self.record.edit_phone("1234567890", "1111111111")
        self.assertEqual(self.record.phones[0].value, "1111111111")

    def test_edit_phone_with_formatting(self):
        self.record.edit_phone("1234567890", "(111) 111-1111")
        self.assertEqual(self.record.phones[0].value, "1111111111")

    def test_edit_phone_not_found_silent(self):
        original_count = len(self.record.phones)
        self.record.edit_phone("5555555555", "1111111111")
        self.assertEqual(len(self.record.phones), original_count)

    def test_edit_phone_invalid_new_phone_raises(self):
        with self.assertRaises(ValueError):
            self.record.edit_phone("1234567890", "abc")


class TestFindPhone(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")
        self.record.add_phone("1234567890")
        self.record.add_phone("9876543210")

    def test_find_phone_success(self):
        phone = self.record.find_phone("1234567890")
        self.assertIsNotNone(phone)
        self.assertEqual(phone.value, "1234567890")

    def test_find_phone_with_formatting(self):
        phone = self.record.find_phone("(123) 456-7890")
        self.assertIsNotNone(phone)
        self.assertEqual(phone.value, "1234567890")

    def test_find_phone_not_found(self):
        phone = self.record.find_phone("5555555555")
        self.assertIsNone(phone)

    def test_find_phone_empty_list(self):
        empty_record = Record("Jane")
        phone = empty_record.find_phone("1234567890")
        self.assertIsNone(phone)

    def test_find_phone_returns_phone_object(self):
        phone = self.record.find_phone("1234567890")
        self.assertIsInstance(phone, Phone)


if __name__ == "__main__":
    unittest.main()
