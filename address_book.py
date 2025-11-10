from collections import UserDict
from datetime import datetime, date, timedelta


class Field:
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return str(self.value)


class Name(Field):
    def __init__(self, value):
        super().__init__(value)


class Phone(Field):
    def __init__(self, value: str):
        super().__init__(value)

        if not value.isdigit():
            raise ValueError("Phone number must contain only digits")
        if len(value) != 10:
            raise ValueError("Phone number must be 10 digits")


class Birthday(Field):
    birthday_format = "%d.%m.%Y"

    def __init__(self, value):
        try:
            birthday = datetime.strptime(str(value),
                                         Birthday.birthday_format).date()
            super().__init__(birthday)
        except ValueError:
            raise ValueError("Invalid date format. Use DD.MM.YYYY")

    def __str__(self):
        return f"{datetime.strftime(self.value, self.birthday_format)}"

    def __repr__(self):
        return datetime.strftime(self.value, self.birthday_format)


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
        return (f"Contact name: {self.name.value}, \n"
                f"phones: {'; '.join(p.value for p in self.phones)} \n"
                f"Birthday: {self.birthday}")


class AddressBook(UserDict):
    def __init__(self):
        super().__init__()

    def add_record(self, record: Record):
        self.data.update({record.name.value: record})

    def find(self, name: str) -> Record | None:
        return self.get(name, None)

    def delete(self, name):
        target_record = self.find(name)
        if target_record is not None:
            self.data.pop(name)

    def get_upcoming_birthdays(self) -> list[dict]:
        today = date.today()
        birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            user_name = record.name
            birthday_str = record.birthday
            og_birthday_date = (
                datetime.strptime(birthday_str.__repr__(),
                                  Birthday.birthday_format).date())

            birthday_date_this_year = (
                date(today.year, og_birthday_date.month, og_birthday_date.day))

            # Check if birthday happens on
            # weekend and add offset for congratulation
            if birthday_date_this_year.isoweekday() == 6:
                birthday_date_this_year += timedelta(days=2)
            elif birthday_date_this_year.isoweekday() == 7:
                birthday_date_this_year += timedelta(days=1)

            date_dif = birthday_date_this_year - today
            # Check only 7 upcoming days including today,
            # ignore b-days in past or further in future
            if 7 >= date_dif.days >= 0:
                birthdays.append(
                    {'name': user_name,
                     'congratulation_date':
                         birthday_date_this_year.strftime("%Y.%m.%d")})

        return birthdays
