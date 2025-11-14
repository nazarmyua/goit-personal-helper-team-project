import unittest

from src.models.email import Email


class TestEmail(unittest.TestCase):
    # VALID CASES

    def test_valid_simple_email(self):
        email = Email("test@example.com")
        self.assertEqual(email.value, "test@example.com")
        self.assertEqual(str(email), "test@example.com")

    def test_valid_email_with_dots_and_plus_and_subdomain(self):
        email = Email("user.name+tag@sub.domain.co")
        self.assertEqual(email.value, "user.name+tag@sub.domain.co")

    def test_email_strips_whitespace(self):
        email = Email("   user@domain.com   ")
        self.assertEqual(email.value, "user@domain.com")

    # INVALID CASES

    def test_email_must_be_string(self):
        with self.assertRaises(ValueError) as ctx:
            Email(123)
        self.assertEqual(str(ctx.exception), "Email must be a string")

    def test_email_cannot_be_empty(self):
        with self.assertRaises(ValueError) as ctx:
            Email("")
        self.assertEqual(str(ctx.exception), "Email can't be empty")

    def test_email_cannot_be_whitespace_only(self):
        with self.assertRaises(ValueError) as ctx:
            Email("   ")
        self.assertEqual(str(ctx.exception), "Email can't be empty")

    def test_email_without_at_symbol(self):
        with self.assertRaises(ValueError) as ctx:
            Email("user.domain.com")
        self.assertEqual(str(ctx.exception), "Email is not valid")

    def test_email_without_domain_part(self):
        with self.assertRaises(ValueError) as ctx:
            Email("user@")
        self.assertEqual(str(ctx.exception), "Email is not valid")

    def test_email_without_local_part(self):
        with self.assertRaises(ValueError) as ctx:
            Email("@domain.com")
        self.assertEqual(str(ctx.exception), "Email is not valid")

    def test_email_with_invalid_tld(self):
        # TLD only 1 char -> should fail our regex
        with self.assertRaises(ValueError) as ctx:
            Email("user@domain.c")
        self.assertEqual(str(ctx.exception), "Email is not valid")


if __name__ == "__main__":
    unittest.main()
