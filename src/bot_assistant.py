from .models import AddressBook, Record
from .decorators import input_error
from .services import absolute_path_provider
import pickle

QUIT_COMMANDS = ["close", "exit", "quit", "q"]
HELP_COMMANDS = ["help", "h"]
HELLO_COMMANDS = ["hello", "hi", "hey"]
ADD_CONTACT = ["add"]
REMOVE_CONTACT = ["remove"]
UPDATE_CONTACT = ["change"]
FIND_CONTACT = ["phone"]
ALL_CONTACTS = ["all"]
ADD_BIRTHDAY = ["add-birthday"]
ADD_NOTE = ["add-note"]
SHOW_BIRTHDAY = ["show-birthday"]
GET_UPCOMING_BIRTHDAYS = ["birthdays"]

CACHE_PATH = absolute_path_provider.get_absolute_path()

@input_error
def parse_input(raw_input: str) -> tuple[str, list[str]]:
    if raw_input == "":
        return "", []

    cmd, *args = raw_input.split()
    cmd = cmd.strip().lower()

    return cmd, *args


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
    name, note, *_ = args
    record = book.find(name)
    record.add_note(note)
    return "Note added."

@input_error
def handle_input(address_book, command, *args):
    if command in QUIT_COMMANDS:
        save_data(address_book)
        print("Good bye!")
        raise KeyboardInterrupt

    elif command in HELLO_COMMANDS:
        print("How can I help you?")

    elif command in HELP_COMMANDS:
        print("Here are the list of commands:"
              f"\nQuit commands: {QUIT_COMMANDS}"
              f"\nHelp commands: {HELP_COMMANDS}"
              f"\nHello commands: {HELLO_COMMANDS}"
              f"\nAdd contact: {ADD_CONTACT} Name Phone. "
              f"\nRemove contact: {REMOVE_CONTACT} Name"
              f"\nUpdate contact: {UPDATE_CONTACT} Name Phone. "
              f"\nFind contact: {FIND_CONTACT} Name. "
              f"\nShow all contacts: {ALL_CONTACTS}"
              f"\nAdd birthday: {ADD_BIRTHDAY} Name dd.mm.yyyy "
              f"\nShow birthday: {SHOW_BIRTHDAY} Name"
              f"\nGet upcoming: {GET_UPCOMING_BIRTHDAYS}"
              f"\nAdd note: {ADD_NOTE} Name"
              )

    elif command in ADD_CONTACT:
        print(add_contact(args, address_book))

    elif command in REMOVE_CONTACT:
        print(remove_contact(args, address_book))

    elif command in UPDATE_CONTACT:
        print(change_contact(args, address_book))

    elif command in FIND_CONTACT:
        print(find_contact(args, address_book))

    elif command in ALL_CONTACTS:
        print(find_all_contacts(address_book))

    elif command in ADD_BIRTHDAY:
        print(add_birthday(args, address_book))

    elif command in SHOW_BIRTHDAY:
        print(show_birthday(args, address_book))

    elif command in GET_UPCOMING_BIRTHDAYS:
        print(get_upcoming_birthdays(address_book))
    
    elif command in ADD_NOTE:
        print(add_note(args, address_book))

    else:
        print("Invalid command. Try again, type 'help' for commands tips")

    # Writing to cache file after each operation to ensure that all data is saved
    save_data(address_book)

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
        return AddressBook()  # Повернення нової адресної книги, якщо файл не знайдено


def main():
    address_book = init_address_book()

    print("Greetings! I'm Jarvis, your personal assistant."
          "\nHow can I help you today?"
          "\nType 'help' for more information.")

    while True:
        user_input = input(">>>")
        command, *args = parse_input(user_input)
        handle_input(address_book, command, *args)

def run():
    # Proxy function to boot up Bot from outer module
    main()


if __name__ == '__main__':
    main()
