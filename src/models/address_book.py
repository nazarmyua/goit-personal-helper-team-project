from collections import UserDict
from datetime import datetime, date, timedelta
import re
import copy

from src.models.record import Record
from src.constants import DATE_FORMAT, REGEX_DATE_FORMAT, REGEX_SHORT_DATE_FORMAT


class AddressBook(UserDict):
    """Stores and manages contact records."""

    def __init__(self):
        super().__init__()

    def add_record(self, record: Record):
        """Add a record to the address book."""
        self.data.update({record.name.value: record})

    def find(self, name: str) -> Record | None:
        """Find a record by contact name."""
        return self.data.get(name, None)

    def search(self, keyword: str) -> list[Record]:
        """Search records by name, phone, or birthday."""
        matches = []
        if keyword == "" or keyword.isspace():
            return matches

        # Searching by birthday date
        if re.match(REGEX_DATE_FORMAT, keyword) or re.match(
            REGEX_SHORT_DATE_FORMAT, keyword
        ):
            for record in self.data.values():
                if (
                    record.birthday is not None
                    and re.search(keyword, record.birthday.__str__()) is not None
                ):
                    matches.append(record)
            return matches

        if keyword.isnumeric():
            # Searching for phone number
            for record in self.data.values():
                for phone_number in record.phones:
                    if re.search(keyword, phone_number.value) is not None:
                        matches.append(record)
        else:
            # Searching for name
            for record in self.data.values():
                if re.search(keyword.lower(), record.name.value.lower()) is not None:
                    matches.append(record)

        return matches

    def delete(self, name):
        """Delete a record by name."""
        target_record = self.find(name)
        if target_record is not None:
            self.data.pop(name)

    def get_upcoming_birthdays(self) -> list[dict]:
        """Get birthdays for the next 7 days."""
        today = date.today()
        birthdays = []

        for record in self.data.values():
            if record.birthday is None:
                continue

            user_name = record.name
            birthday_str = record.birthday
            og_birthday_date = datetime.strptime(
                birthday_str.__repr__(), DATE_FORMAT
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

    def get_records_by_note_keyword(self, keyword: str) -> list[Record]:
        """Find records by keyword in notes."""
        matches = []
        keyword = keyword.strip()
        if not keyword:
            return matches

        for record in self.data.values():
            matching_notes = {
                note_id: note
                for note_id, note in record.notes.items()
                if keyword.lower() in note.value.lower()
            }
            if matching_notes:
                filtered_record = copy.copy(record)
                filtered_record.notes = matching_notes
                matches.append(filtered_record)

        return matches
