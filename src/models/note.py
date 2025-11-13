from .tag import Tag
from .field import Field


class Note(Field):
    def __init__(self, note_value):
        super().__init__(note_value)

        self._tags = []

    @Field.value.setter
    def value(self, value):
        if not value.strip():
            raise ValueError("Note value can't be empty")
        self._value = value.strip()

    def add_tags(self, tags: list[str]):
        new_tags = [Tag(tag) for tag in tags]
        self._tags.extend(new_tags)

    def remove_tag(self, tag: str):
        self._tags = [t for t in self._tags if t.value != tag]

    def get_tags(self) -> list[Tag]:
        return self._tags
