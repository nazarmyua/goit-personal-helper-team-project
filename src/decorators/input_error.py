from src.utils.logger import error, warning


def _handle_key_error(func_name: str, error: KeyError, not_exist_functions: set) -> str:
    """Generate appropriate error message for KeyError."""
    if func_name in {"edit_note", "remove_note", "add_tags_to_note"} and error.args:
        return str(error)

    if func_name in not_exist_functions:
        return "This contact does not exist"

    return "Record with this Id does not exist"


def _handle_attribute_error(
    func_name: str, error: AttributeError, not_exist_functions: set
) -> str | None:
    """Generate appropriate error message for AttributeError."""
    if func_name == "show_birthday":
        msg = str(error)
        if "name" in msg:
            return "This contact does not exist"
        if "birthday" in msg:
            return "This contact does not have a birthday record"

    if func_name in not_exist_functions:
        return "This contact does not exist"

    return None


def input_error(func):
    """Decorator that handles common input errors and exceptions."""
    messages = {
        "add_contact": "Please provide Name and phone number",
        "add_birthday": "Please provide Name and date in format dd.mm.yyyy",
        "change_contact": "Please provide Name, old number and new number",
        "show_birthday": "Please provide Name",
        "find_contact": "Please provide Name",
        "remove_contact": "Please provide Name",
        "add_note": "Please provide Name and note",
        "edit_note": "Please provide Name, note index and new note",
        "add_tags_to_note": "Please provide Name, note index and at least one tag",
        "remove_note": "Please provide Name and note index",
        "search_notes": "Please provide keyword to search",
    }

    not_exist_functions = {
        "show_birthday",
        "find_contact",
        "remove_contact",
        "add_note",
        "edit_note",
        "remove_note",
        "search_notes",
        "add_tags_to_note",
    }

    def inner(*args, **kwargs):
        try:
            return func(*args, **kwargs)

        except (IndexError, TypeError):
            return warning(messages.get(func.__name__, "Not enough arguments"))

        except ValueError as e:
            if e.args:
                return error(str(e))
            return error("Invalid value")

        except KeyError as e:
            return _handle_key_error(func.__name__, e, not_exist_functions)

        except AttributeError as e:
            msg = _handle_attribute_error(func.__name__, e, not_exist_functions)
            if msg is not None:
                return msg
            else:
                return f"{error(str(e))}"

        except KeyboardInterrupt:
            quit()

    return inner
