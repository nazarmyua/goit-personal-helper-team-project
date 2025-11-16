import re

from src.models.field import Field


def is_valid_phone_regex(phone_number: str) -> bool:
    #    Simple generic phone validation:
    #     - Allows optional '+' at the beginning
    #     - Allows spaces, dashes, dots, parentheses as separators
    #     - After cleaning, there must be 10–15 digits

    if not isinstance(phone_number, str):
        return False

    phone_number = phone_number.strip()
    if not phone_number:
        return False

    # Remove common separators: space, dash, dot, parentheses
    cleaned = re.sub(r"[()\s.-]", "", phone_number)

    # Optional leading '+'
    if cleaned.startswith("+"):
        cleaned = cleaned[1:]

    if not cleaned.isdigit():
        return False

    return 10 <= len(cleaned) <= 15


class Phone(Field):
    @Field.value.setter
    def value(self, phone_raw: str):
        if not isinstance(phone_raw, str):
            raise ValueError("Phone number must be a string")

        phone_raw = phone_raw.strip()
        if not phone_raw:
            raise ValueError("Phone number cannot be empty")

        if not is_valid_phone_regex(phone_raw):
            raise ValueError("Invalid phone number format")

        digits_only = "".join(ch for ch in phone_raw if ch.isdigit())

        if len(digits_only) < 10:
            raise ValueError("Phone number must contain at least 10 digits")

        self._value = digits_only

    def __str__(self):
        return self.value
