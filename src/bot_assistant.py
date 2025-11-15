from colorama import Fore, Style, init
from .models import AddressBook, Record
from .decorators import input_error
from .services import absolute_path_provider
from src.utils.logger import success, info, error, simple_text
import pickle
from cmd import Cmd

CACHE_PATH = absolute_path_provider.get_absolute_path()

init(autoreset=True)


@input_error
def add_contact(args, book: AddressBook):
    if len(args) < 2:
        raise ValueError(error("Please provide Name and phone number"))

    name, phone, email, *_ = args

    record = book.find(name)
    message = success(f"Contact for {name} is updated.")
    if record is None:
        record = Record(name)
        book.add_record(record)
        message = success(f"Contact for {name} is added.")

    if phone:
        record.add_phone(phone)

    if email:
        record.add_email(email)

    return message


@input_error
def remove_contact(args, book: AddressBook) -> str:
    name, *_ = args
    book.delete(name)
    return success("Contact removed: {}".format(name))


@input_error
def change_contact(args, book: AddressBook) -> str:
    if len(args) < 3:
        raise ValueError(error("Please provide Name, old number and new number"))

    name, old_phone, new_phone, new_email, *_ = args

    record = book.find(name)

    record.edit_phone(old_phone, new_phone)

    if new_email is not None:
        record.edit_email(new_email)

    return success("Contact updated.")


@input_error
def find_contact(args, book: AddressBook) -> str:
    keyword, *_ = args

    records = book.search(keyword)

    if len(records) == 0:
        return error(f"Nothing was found by keyword '{keyword}'")

    all_contacts_str = ""
    for record in records:
        all_contacts_str += f"\n{record}\n"
    return simple_text(all_contacts_str)


@input_error
def find_all_contacts(book: AddressBook) -> str:
    if len(book) == 0:
        return info("Contacts book is empty")

    all_contacts_str = ""
    for name, record in book.items():
        all_contacts_str += f"{record}\n"
    return simple_text(all_contacts_str)


@input_error
def add_birthday(args, book: AddressBook) -> str:
    name, birthday, *_ = args
    record = book.find(name)
    record.add_birthday(birthday)
    return success("Birthday added.")


@input_error
def show_birthday(args, book: AddressBook) -> str:
    name, *_ = args
    record = book.find(name)
    return simple_text(f"{record.name} - {record.birthday}")


@input_error
def get_upcoming_birthdays(book: AddressBook) -> str:
    upcoming_birthdays = book.get_upcoming_birthdays()
    to_congratulate = "Next 7 days birthdays:"
    for b_day in upcoming_birthdays:
        to_congratulate += f"\n{b_day['name']} {b_day['congratulation_date']}"

    return simple_text(to_congratulate)


@input_error
def add_note(args, book: AddressBook) -> str:
    name, *note_parts = args
    note = " ".join(note_parts)
    book.find(name).add_note(note)
    return success("Note added.")


@input_error
def edit_note(args, book: AddressBook) -> str:
    name, id, *note_parts = args
    new_note = " ".join(note_parts)
    record = book.find(name)
    record.edit_note(int(id), new_note)
    return success("Note edited.")


@input_error
def remove_note(args, book: AddressBook) -> str:
    name, id, *_ = args
    record = book.find(name)
    record.remove_note(int(id))
    return success("Note removed.")


@input_error
def search_notes(args, book: AddressBook) -> str:
    keyword, *_ = args
    records = book.get_records_by_note_keyword(keyword)

    if not records:
        return error(f"No notes found containing '{keyword}'.")

    result_lines = []
    for record in records:
        result_lines.append(f"\n{record}\n")

    result_text = "".join(result_lines)
    return simple_text(
        f"Found {len(records)} record(s) with notes containing '{keyword}':\n{result_text}"
    )


@input_error
def add_tags_to_note(args, book: AddressBook) -> str:
    name, id, *tags = args
    record = book.find(name)
    record.add_tags_to_note(int(id), tags)
    return success("Tags added to note.")


@input_error
def remove_tag_from_note(args, book: AddressBook) -> str:
    name, id, tag = args
    record = book.find(name)
    record.remove_tag_from_note(int(id), tag)
    return success("Tag removed from note.")


@input_error
def get_notes_by_tag(args, book: AddressBook) -> str:
    name, tag = args
    record = book.find(name)
    notes_str = record.find_note_by_tag(tag)
    if not notes_str:
        return error(f"No notes found with tag '{tag}'")
    return simple_text(notes_str)


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


class BotAssistant(Cmd):
    prompt = ">>> "
    address_book = init_address_book()

    def postcmd(self, stop, line):
        save_data(self.address_book)
        return stop

    def do_hello(self, arg):
        print(simple_text("How can I help you?"))

    def help_hello(self):
        print(simple_text("Print greeting message"))

    def do_quit(self, arg):
        save_data(self.address_book)
        print(success("Good bye!"))
        return True

    def help_quit(self):
        print(simple_text("Quit the program"))

    def do_add(self, arg):
        print(add_contact(arg.split(), self.address_book))

    def help_add(self):
        print(simple_text("Add a new contact"))

    def do_remove(self, arg):
        print(remove_contact(arg.split(), self.address_book))

    def help_remove(self):
        print(simple_text("Remove a contact"))

    def do_change(self, arg):
        print(change_contact(arg.split(), self.address_book))

    def help_change(self):
        print(simple_text("Change a contact's phone number"))

    def do_find(self, arg):
        print(find_contact(arg.split(), self.address_book))

    def help_find(self):
        print(simple_text("Find a contact by name"))

    def do_phone(self, arg):
        self.do_find(arg)

    def help_phone(self):
        print(simple_text("Find a contact by name"))

    def do_birthdays(self, arg):
        print(get_upcoming_birthdays(self.address_book))

    def help_birthdays(self):
        print(simple_text("Get upcoming birthdays for the next 7 days"))

    def do_all(self, arg):
        print(find_all_contacts(self.address_book))

    def help_all(self):
        print(simple_text("Get all contacts"))

    def do_add_birthday(self, arg):
        print(add_birthday(arg.split(), self.address_book))

    def help_add_birthday(self):
        print(simple_text("Add a birthday to a contact"))

    def do_show_birthday(self, arg):
        print(show_birthday(arg.split(), self.address_book))

    def help_show_birthday(self):
        print(simple_text("Show a birthday of a contact"))

    def do_get_upcoming(self, arg):
        print(get_upcoming_birthdays(self.address_book))

    def help_get_upcoming(self):
        print(simple_text("Get upcoming birthdays for the next 7 days"))

    def do_add_note(self, arg):
        print(add_note(arg.split(), self.address_book))

    def help_add_note(self):
        print(simple_text("Add a note to a contact"))

    def do_search_notes(self, arg):
        print(search_notes(arg.split(), self.address_book))

    def help_search_notes(self):
        print(simple_text("Search notes by keyword"))

    def do_remove_note(self, arg):
        print(remove_note(arg.split(), self.address_book))

    def help_remove_note(self):
        print(simple_text("Remove a note from a contact"))

    def do_edit_note(self, arg):
        print(edit_note(arg.split(), self.address_book))

    def help_edit_note(self):
        print(simple_text("Edit a note of a contact"))

    def do_add_tags_to_note(self, arg):
        print(add_tags_to_note(arg.split(), self.address_book))

    def help_add_tags_to_note(self):
        print(simple_text("Add tags to a note of a contact"))

    def do_remove_tag_from_note(self, arg):
        print(remove_tag_from_note(arg.split(), self.address_book))

    def help_remove_tag_from_note(self):
        print(simple_text("Remove a tag from a note of a contact"))

    def do_get_notes_by_tag(self, arg):
        print(get_notes_by_tag(arg.split(), self.address_book))

    def help_get_notes_by_tag(self):
        print(simple_text("Get notes by tag of a contact"))


def main():
    print(
        f"Greetings! I'm {Fore.YELLOW}Jarvis{Style.RESET_ALL}, your personal assistant."
        "\nHow can I help you today?"
        f"\nType {Fore.BLUE}'help'{Style.RESET_ALL} for more information."
    )

    BotAssistant().cmdloop()


def run():
    # Proxy function to boot up Bot from outer module
    main()


if __name__ == "__main__":
    main()
