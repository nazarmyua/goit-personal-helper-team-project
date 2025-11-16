from src.models.name import Name
from src.models.phone import Phone
from src.models.birthday import Birthday
from src.models.note import Note
from src.models.email import Email


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.notes = {}
        self.email = None

    def add_phone(self, phone: str):
        match_phone = self.find_phone(phone)
        if match_phone is None:
            self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        match_phone = self.find_phone(phone)
        if match_phone:
            self.phones.remove(match_phone)

    def edit_phone(self, phone, new_phone):
        match_phone = self.find_phone(phone)
        if match_phone:
            index = self.phones.index(match_phone)
            self.phones[index] = Phone(new_phone)

    def find_phone(self, target_phone):
        target_phone = "".join(ch for ch in target_phone if ch.isdigit())
        for phone in self.phones:
            if phone.value == target_phone:
                return phone

        return None

    def add_email(self, email: str):
        self.email = Email(email)

    def edit_email(self, new_email: str):
        self.email = Email(new_email)

    def add_note(self, note):
        next_id = max(self.notes.keys(), default=0) + 1
        self.notes[next_id] = Note(note)

    def edit_note(self, note_id, new_value):
        if note_id not in self.notes:
            raise KeyError(f"Note with id {note_id} not found")

        self.notes[note_id] = Note(new_value)

    def remove_note(self, note_id):
        if note_id not in self.notes:
            raise KeyError(f"Note with id {note_id} not found")

        del self.notes[note_id]

    def add_tags_to_note(self, note_id, tag: list[str]):
        if note_id not in self.notes:
            raise KeyError(f"Note with id {note_id} not found")

        self.notes[note_id].add_tags(tag)

    def remove_tag_from_note(self, note_id, tag: str):
        if note_id not in self.notes:
            raise KeyError(f"Note with id {note_id} not found")

        self.notes[note_id].remove_tag(tag)

    def find_note_by_tag(self, tag: str) -> {Note}:
        matched_notes = {}
        for note_id, note in self.notes.items():
            for note_tag in note.get_tags():
                if note_tag.value == tag:
                    matched_notes[note_id] = note
        return self.show_info(matched_notes)

    def get_formatered_notes(self, notes) -> str:
        if not notes:
            return ""

        header = "  ID | Note" + " " * 40 + " | Tags\n"
        rows = [
            f"{note_id:>4} | {note.value:<44} | {'; '.join(p.value for p in note.get_tags())}"
            for note_id, note in notes.items()
        ]
        return "\n" + header + "\n" + "\n".join(rows)

    def show_info(self, notes) -> str:
        notes_str = self.get_formatered_notes(notes)

        return (
            "\n"
            f"{'Contact name:':<15} {self.name.value}\n"
            f"{'Phones:':<15} {'; '.join(p.value for p in self.phones)}\n"
            f"{'Email:':<15} {self.email if self.email else ''}\n"
            f"{'Birthday:':<15} {self.birthday}\n"
            f"{'Notes:':<15}{notes_str}"
        )

    def __str__(self):
        return self.show_info(self.notes)
