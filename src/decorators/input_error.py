def input_error(func):
    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError:
            if func.__name__ == "add_contact":
                return "Please provide Name and phone number"
            if func.__name__ == "add_birthday":
                return "Please provide Name and date in format dd.mm.yyyy"
            if func.__name__ == "add_note":
                return "Please provide Name and note"
            if func.__name__ == "change_contact":
                return "Please provide Name, old number and new number"
            if func.__name__ in ("show_birthday", "find_contact", "remove_contact"):
                return "Please provide Name"
            else:
                raise
        except AttributeError as e:
            if func.__name__ in "show_birthday":
                if "name" in e.args[0]:
                    return "This contact does not exist"
                elif "birthday" in e.args[0]:
                    return "This contact does not have a birthday record"

            if func.__name__ in [
                "show_birthday",
                "find_contact",
                "remove_contact",
                "change_contact",
            ]:
                return "This contact does not exist"

        except KeyboardInterrupt:
            quit()

    return inner
