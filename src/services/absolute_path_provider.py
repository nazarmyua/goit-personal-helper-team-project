from pathlib import Path


def get_absolute_path() -> str:
    user_dir = Path.home()

    cache_folder = user_dir / "AddressBookCache"
    cache_folder.mkdir(exist_ok=True)  # Create if not existing

    file_path = cache_folder / "address_book.pkl"
    return str(file_path)
