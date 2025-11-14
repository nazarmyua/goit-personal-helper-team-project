import unittest
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


if __name__ == "__main__":
    unittest.main()
