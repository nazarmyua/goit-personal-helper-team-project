from .models import AddressBook, Record
from .decorators import input_error
from .services import absolute_path_provider
import pickle
import cmd

CACHE_PATH = absolute_path_provider.get_absolute_path()


@input_error
def add_contact(args, book: AddressBook):
    name, phone, *_ = args
    record = book.find(name)
    message = "Contact updated."
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = "Contact added."
    if phone:
        record.add_phone(phone)
    return message


@input_error
def remove_contact(args, book: AddressBook) -> str:
    name, *_ = args
    book.delete(name)
    return "Contact removed: {}".format(name)


@input_error
def change_contact(args, book: AddressBook) -> str:
    name, old_phone, new_phone, *_ = args

    record = book.find(name)
    record.edit_phone(old_phone, new_phone)
    return "Phone changed."


@input_error
def find_contact(args, book: AddressBook) -> Record | None:
    name, *_ = args
    record = book.find(name)
    return record


@input_error
def find_all_contacts(book: AddressBook) -> str:
    if len(book) == 0:
        return "Contacts book is empty"

    all_contacts_str = ""
    for name, record in book.items():
        all_contacts_str += f"{record}\n"
    return all_contacts_str


@input_error
def add_birthday(args, book: AddressBook) -> str:
    name, birthday, *_ = args
    record = book.find(name)
    record.add_birthday(birthday)
    return "Birthday added."


@input_error
def show_birthday(args, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    return f"{record.name} - {record.birthday}"


@input_error
def get_upcoming_birthdays(book: AddressBook) -> str:
    upcoming_birthdays = book.get_upcoming_birthdays()
    to_congratulate = "Next 7 days birthdays:"
    for b_day in upcoming_birthdays:
        to_congratulate += f"\n{b_day['name']} {b_day['congratulation_date']}"

    return to_congratulate


@input_error
def add_note(args, book: AddressBook) -> str:
    name, *note_parts = args
    note = " ".join(note_parts)
    book.find(name).add_note(note)
    return "Note added."


@input_error
def edit_note(args, book: AddressBook) -> str:
    name, id, *note_parts = args
    new_note = " ".join(note_parts)
    record = book.find(name)
    record.edit_note(int(id), new_note)
    return "Note edited."


def init_address_book() -> AddressBook:
    try:
        with open(CACHE_PATH, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError or pickle.UnpicklingError:
        return AddressBook()


def save_data(book):
    with open(CACHE_PATH, "wb") as f:
        pickle.dump(book, f)


def load_data():
    try:
        with open(CACHE_PATH, "rb") as f:
            return pickle.load(f)
    except FileNotFoundError:
        # Повернення нової адресної книги, якщо файл не знайдено
        return AddressBook()


class BotAssistant(cmd.Cmd):
    prompt = ">>> "
    address_book = init_address_book()

    def postcmd(self, stop, line):
        save_data(self.address_book)
        return stop

    def do_hello(self, arg):
        print("How can I help you?")

    def help_hello(self):
        print("Print greeting message")

    def do_quit(self, arg):
        save_data(self.address_book)
        print("Good bye!")
        return True

    def help_quit(self):
        print("Quit the program")

    def do_add(self, arg):
        print(add_contact(arg.split(), self.address_book))

    def help_add(self):
        print("Add a new contact")

    def do_remove(self, arg):
        print(remove_contact(arg.split(), self.address_book))

    def help_remove(self):
        print("Remove a contact")

    def do_change(self, arg):
        print(change_contact(arg.split(), self.address_book))

    def help_change(self):
        print("Change a contact's phone number")

    def do_find(self, arg):
        print(find_contact(arg.split(), self.address_book))

    def help_find(self):
        print("Find a contact by name")

    def do_phone(self, arg):
        self.do_find(arg)

    def help_phone(self):
        print("Find a contact by name")

    def do_birthdays(self, arg):
        print(get_upcoming_birthdays(self.address_book))

    def help_birthdays(self):
        print("Get upcoming birthdays for the next 7 days")

    def do_all(self, arg):
        print(find_all_contacts(self.address_book))

    def help_all(self):
        print("Get all contacts")

    def do_add_birthday(self, arg):
        print(add_birthday(arg.split(), self.address_book))

    def help_add_birthday(self):
        print("Add a birthday to a contact")

    def do_show_birthday(self, arg):
        print(show_birthday(arg.split(), self.address_book))

    def help_show_birthday(self):
        print("Show a birthday of a contact")

    def do_get_upcoming(self, arg):
        print(get_upcoming_birthdays(self.address_book))

    def help_get_upcoming(self):
        print("Get upcoming birthdays for the next 7 days")

    def do_add_note(self, arg):
        print(add_note(arg.split(), self.address_book))

    def help_add_note(self):
        print("Add a note to a contact")

    def do_edit_note(self, arg):
        print(edit_note(arg.split(), self.address_book))

    def help_edit_note(self):
        print("Edit a note of a contact")


bot_assistant = BotAssistant()


# @input_error
def handle_input(address_book, line):
    bot_assistant.address_book = address_book
    bot_assistant.onecmd(line)


def main():
    print(
        "Greetings! I'm Jarvis, your personal assistant."
        "\nHow can I help you today?"
        "\nType 'help' for more information."
    )

    bot_assistant.cmdloop()


def run():
    # Proxy function to boot up Bot from outer module
    main()


if __name__ == "__main__":
    main()
