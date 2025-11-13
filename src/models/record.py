from .name import Name
from .phone import Phone
from .birthday import Birthday
from .note import Note


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None
        self.notes = {}

    def add_phone(self, phone: str):
        match_phone = self.find_phone(phone)
        if match_phone is None:
            self.phones.append(Phone(phone))

    def add_birthday(self, birthday):
        self.birthday = Birthday(birthday)

    def remove_phone(self, phone):
        match_phone = self.find_phone(phone)
        if match_phone:
            self.phones.remove(phone)

    def edit_phone(self, phone, new_phone):
        match_phone = self.find_phone(phone)
        if match_phone:
            index = self.phones.index(match_phone)
            self.phones[index] = Phone(new_phone)

    def find_phone(self, target_phone):
        for phone in self.phones:
            if phone.value == target_phone:
                return phone

        return None

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

    def __str__(self):
        if self.notes:
            header = "  ID | Note\n" + "-" * 20
            rows = [
                f"{note_id:>4} | {note.value}"
                for note_id, note in self.notes.items()
            ]
            notes_str = "\n" + header + "\n" + "\n".join(rows)
        else:
            notes_str = ""

        return (
            f"{'Contact name:':<15} {self.name.value}\n"
            f"{'Phones:':<15} {'; '.join(p.value for p in self.phones)}\n"
            f"{'Birthday:':<15} {self.birthday}\n"
            f"{'Notes:':<15}{notes_str}"
        )
