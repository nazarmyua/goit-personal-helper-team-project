import re

from src.models.field import Field

EMAIL_REGEX = re.compile(r"^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}$")


class Email(Field):
    @Field.value.setter
    def value(self, value):
        if not isinstance(value, str):
            raise ValueError("Email must be a string")

        value = value.strip()

        if not value:
            raise ValueError("Email can't be empty")

        if not EMAIL_REGEX.match(value):
            raise ValueError("Email is not valid")

        self._value = value

    def __str__(self):
        return self.value
