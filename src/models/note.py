from .field import Field

class Note(Field):
    @Field.value.setter
    def value(self, value):
        if not value.strip():
            raise ValueError("Note value can't be empty")
        self._value = value.strip()