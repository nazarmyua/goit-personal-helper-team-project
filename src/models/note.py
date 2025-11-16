from src.models.tag import Tag
from src.models.field import Field


class Note(Field):
    """Represents a note with optional tags."""

    def __init__(self, note_value):
        super().__init__(note_value)

        self._tags = []

    @Field.value.setter
    def value(self, value):
        if not value.strip():
            raise ValueError("Note value can't be empty")
        self._value = value.strip()

    def add_tags(self, tags: list[str]):
        """Add tags to the note."""
        new_tags = [Tag(tag) for tag in tags]
        self._tags.extend(new_tags)

    def remove_tag(self, tag: str):
        """Remove a tag from the note."""
        self._tags = [t for t in self._tags if t.value != tag]

    def get_tags(self) -> list[Tag]:
        """Get all tags assigned to this note."""
        return self._tags
