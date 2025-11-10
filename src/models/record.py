from .name import Name
from .phone import Phone
from .birthday import Birthday


class Record:
    def __init__(self, name):
        self.name = Name(name)
        self.phones = []
        self.birthday = None

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

    def __str__(self):
        return (
            f"Contact name: {self.name.value}, \n"
            f"phones: {'; '.join(p.value for p in self.phones)} \n"
            f"Birthday: {self.birthday}"
        )
