from collections import UserDict
from datetime import datetime, date, timedelta

from .record import Record
from .birthday import Birthday


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
            og_birthday_date = datetime.strptime(
                birthday_str.__repr__(), Birthday.birthday_format
            ).date()

            birthday_date_this_year = date(
                today.year, og_birthday_date.month, og_birthday_date.day
            )

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
                    {
                        "name": user_name,
                        "congratulation_date": birthday_date_this_year.strftime(
                            "%Y.%m.%d"
                        ),
                    }
                )

        return birthdays
