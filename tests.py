from src.bot_assistant import handle_input
from src.models import AddressBook


def main():
    run_tests(AddressBook())


def execute(str_input, address_book):
    handle_input(address_book, str_input)


def run_tests(address_book: AddressBook) -> None:
    # Add Mike
    execute("add Mike 1234567890", address_book)

    # Add him a birthday
    execute("add_birthday Mike 05.11.1997", address_book)

    # Print his birthday
    execute("show_birthday Mike", address_book)

    # Add Kate
    execute("add Kate 1111111111", address_book)

    # Add her extra number
    execute("add Kate 1111111112", address_book)

    # Add her b-day
    execute("add_birthday Kate 04.11.1991", address_book)

    # Add Paolinka without birthday
    execute("add Paolinka 1111111113", address_book)

    # Print all records
    execute("all", address_book)

    # Change Mikes number and print updated number
    execute("change Mike 1234567890 0987654321", address_book)
    execute("phone Mike", address_book)
    # Get all upcoming b-days
    execute("birthdays", address_book)

    # Add and remove Jovani, check that he is removed
    execute("add Jovani 1111111112", address_book)
    execute("remove Jovani", address_book)
    execute("all", address_book)

    # Input mistakes
    execute("add Jovani 111111111", address_book)

    execute("add Jovani OneOneOne", address_book)

    execute("remove Jovani", address_book)
    execute("remove Jovani please 123", address_book)

    execute("phone Jovani", address_book)

    execute("show_birthday Jovani", address_book)

    execute("show_birthday", address_book)
    execute("show_birthday ", address_book)
    execute("phone", address_book)
    execute("phone ", address_book)
    execute("add", address_book)
    execute("add ", address_book)
    execute("remove", address_book)
    execute("remove ", address_book)
    execute("add_birthday ", address_book)

    execute("add_birthday Jovani", address_book)
    execute("add_birthday Mike 20-11-1997", address_book)
    execute("add_birthday Mike 20-11", address_book)
    execute("add_birthday Mike ", address_book)

    execute("change", address_book)
    execute("change ", address_book)
    execute("change Jovani ", address_book)

    execute("remove 1", address_book)
    execute("change 2", address_book)

    execute("a", address_book)
    execute("", address_book)

    execute("add Stephan 1231233330", address_book)
    execute("show-birthday Stephan", address_book)
    execute("birthdays", address_book)

    print("\n")

    execute("show_birthday Nicolaos", address_book)
    execute("show_birthday Nicolaos 20.11.1997", address_book)
    execute("change Nicolaos 1231231231 3213213213", address_book)
    execute("phone Nicolaos", address_book)
    execute("remove Nicolaos", address_book)


if __name__ == "__main__":
    main()
