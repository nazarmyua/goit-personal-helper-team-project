from datetime import datetime

from src.models.field import Field
from src.constants import DATE_FORMAT


class Birthday(Field):
    """Represents a birthday field in DD.MM.YYYY format."""

    @Field.value.setter
    def value(self, value):
        try:
            self._value = datetime.strptime(value, DATE_FORMAT)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return f"{datetime.strftime(self.value, DATE_FORMAT)}"

    def __repr__(self):
        return datetime.strftime(self.value, DATE_FORMAT)
