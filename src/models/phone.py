from .field import Field


class Phone(Field):
    @Field.value.setter
    def value(self, value):
        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10:
            raise ValueError("Phone number must be 10 digits")
        self._value = value

    def __str__(self):
        return f"{self.value}"
