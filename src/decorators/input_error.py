def input_error(func):
    messages = {
        "add_contact": "Please provide Name and phone number",
        "add_birthday": "Please provide Name and date in format dd.mm.yyyy",
        "change_contact": "Please provide Name, old number and new number",
        "show_birthday": "Please provide Name",
        "find_contact": "Please provide Name",
        "remove_contact": "Please provide Name",
        "add_note": "Please provide Name and note",
        "edit_note": "Please provide Name, note index and new note",
    }

    not_exist_functions = {
        "show_birthday",
        "find_contact",
        "remove_contact",
        "change_contact",
    }

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except ValueError:
            return messages.get(func.__name__, "Invalid input")

        except AttributeError as e:
            if func.__name__ == "show_birthday":
                if "name" in str(e):
                    return "This contact does not exist"
                if "birthday" in str(e):
                    return "This contact does not have a birthday record"

            if func.__name__ in not_exist_functions:
                return "This contact does not exist"

        except KeyboardInterrupt:
            quit()

    return inner
