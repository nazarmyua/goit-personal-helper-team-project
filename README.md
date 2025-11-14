# Personal Helper Bot Assistant - Jarvis

A command-line personal assistant for managing contacts, birthdays, and notes with an interactive interface.

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Quick Start](#quick-start)
- [Command Reference](#command-reference)
- [Usage Examples](#usage-examples)
- [Data Storage](#data-storage)
- [Testing](#testing)
- [Troubleshooting](#troubleshooting)

---

## Features

**Contact Management**
- Add, remove, and update contacts with multiple phone numbers
- Search by name, phone number, or birthday
- View all contacts

**Birthday Management**
- Track birthdays with DD.MM.YYYY format
- View upcoming birthdays (next 7 days)
- Automatic weekend adjustment (moves to Monday)

**Note Management**
- Add/edit/remove notes for contacts
- Tag notes for organization
- Search notes by keyword or tag

**Additional Features**
- Persistent data storage (auto-save)
- Input validation with error messages
- Built-in help system
- Command history support

---

## Installation

### Prerequisites
- Python 3.10 or higher

### Steps

```bash
# Clone repository
git clone https://github.com/nazarmyua/goit-personal-helper-team-project.git
cd goit-personal-helper-team-project

# Install dependencies (if any in requirements.txt)
pip install -r requirements.txt

# Run application
python main.py
```

---

## Quick Start

### Starting the Bot

```bash
python main.py
```

Output:
```
Greetings! I'm Jarvis, your personal assistant.
How can I help you today?
Type 'help' for more information.
>>> 
```

### Getting Help

```
>>> help                    # List all commands
>>> help <command>          # Help for specific command
```

### Exiting

```
>>> quit    # or exit, or Ctrl+D (Linux/Mac), Ctrl+Z (Windows)
```

---

## Command Reference

### Contact Commands

| Command | Syntax | Description |
|---------|--------|-------------|
| `add` | `add <name> <phone>` | Add contact or phone to existing contact |
| `change` | `change <name> <old_phone> <new_phone>` | Change phone number |
| `remove` | `remove <name>` | Remove contact |
| `find` | `find <keyword>` | Search by name, phone, or birthday |
| `phone` | `phone <keyword>` | Alias for find |
| `all` | `all` | Show all contacts |

**Examples:**
```
>>> add John 1234567890
>>> change John 1234567890 1111111111
>>> remove John
>>> find John
>>> all
```

**Phone Format:** 10 digits, no spaces or special characters

---

### Birthday Commands

| Command | Syntax | Description |
|---------|--------|-------------|
| `add_birthday` | `add_birthday <name> <date>` | Add birthday (DD.MM.YYYY) |
| `show_birthday` | `show_birthday <name>` | Show contact's birthday |
| `birthdays` | `birthdays` | Upcoming birthdays (7 days) |
| `get_upcoming` | `get_upcoming` | Alias for birthdays |

**Examples:**
```
>>> add_birthday John 15.03.1990
>>> show_birthday John
>>> birthdays
```

**Date Format:** DD.MM.YYYY (e.g., 15.03.1990)

---

### Note Commands

| Command | Syntax | Description |
|---------|--------|-------------|
| `add_note` | `add_note <name> <text>` | Add note to contact |
| `edit_note` | `edit_note <name> <id> <text>` | Edit note by ID |
| `remove_note` | `remove_note <name> <id>` | Remove note by ID |
| `search_notes` | `search_notes <keyword>` | Search notes across all contacts |

**Examples:**
```
>>> add_note John Meeting at 3pm
>>> edit_note John 1 Meeting at 4pm
>>> remove_note John 1
>>> search_notes meeting
```

---

### Tag Commands

| Command | Syntax | Description |
|---------|--------|-------------|
| `add_tags_to_note` | `add_tags_to_note <name> <id> <tag1> [tag2]...` | Add tags to note |
| `remove_tag_from_note` | `remove_tag_from_note <name> <id> <tag>` | Remove tag from note |
| `get_notes_by_tag` | `get_notes_by_tag <name> <tag>` | Find notes by tag |

**Examples:**
```
>>> add_tags_to_note John 1 work urgent
>>> remove_tag_from_note John 1 urgent
>>> get_notes_by_tag John work
```

---

### System Commands

| Command | Description |
|---------|-------------|
| `hello` | Display greeting |
| `quit` or `exit` | Save and exit |
| `help` | Show all commands |
| `help <command>` | Help for specific command |

---

## Usage Examples

### Example 1: Managing a Contact

```bash
# Add contact with phone
>>> add Alice 1234567890
Contact added.

# Add birthday
>>> add_birthday Alice 15.05.1992
Birthday added.

# Add second phone
>>> add Alice 0987654321
Contact updated.

# Add note with tags
>>> add_note Alice Call about project
Note added.

>>> add_tags_to_note Alice 1 work important
Tags added to note.

# View contact
>>> find Alice

Contact name:   Alice
Phones:         1234567890; 0987654321
Birthday:       15.05.1992
Notes:          
  ID | Note                                         | Tags
     1 | Call about project                          | work; important
```

---

### Example 2: Birthday Tracking

```bash
# Add contacts with birthdays
>>> add Bob 1111111111
>>> add_birthday Bob 16.11.2025

>>> add Carol 2222222222
>>> add_birthday Carol 18.11.2025

# Check upcoming birthdays
>>> birthdays
Next 7 days birthdays:
Bob 2025.11.18
Carol 2025.11.18
```

---

### Example 3: Note Organization

```bash
# Add contact
>>> add David 3333333333

# Add notes with tags
>>> add_note David Buy groceries
>>> add_tags_to_note David 1 personal shopping

>>> add_note David Finish report
>>> add_tags_to_note David 2 work urgent

# Search notes
>>> search_notes report
Found 1 record(s) with notes containing 'report':
[Shows David's note]

# Filter by tag
>>> get_notes_by_tag David work
[Shows work-tagged notes]

# Edit note
>>> edit_note David 2 Submit quarterly report
Note edited.
```

---

### Example 4: Search Features

```bash
# Search by name fragment
>>> find Ali
[Returns Alice, Alison, etc.]

# Search by phone digits
>>> find 555
[Returns contacts with "555" in phone]

# Search by birthday
>>> find 15.05
[Returns contacts with May 15th birthday]
```

---

## Data Storage

### Location
Data stored at: `~/AddressBookCache/address_book.pkl`  
(in your user directory's AddressBookCache folder)

The folder is automatically created on first run if it doesn't exist.

### Auto-Save
- Saves automatically after every command
- Data persists between sessions
- No manual save needed

### Backup
```bash
# Backup your data
cp ~/AddressBookCache/address_book.pkl ~/AddressBookCache/address_book_backup.pkl

# Or specify full path
cp ~/AddressBookCache/address_book.pkl ~/Documents/jarvis_backup.pkl
```

### Recovery
If corrupted, delete the file and restart:
```bash
rm ~/AddressBookCache/address_book.pkl
python main.py  # Creates fresh database
```

### Finding Your Data
```bash
# On Linux/Mac
ls ~/AddressBookCache/

# On Windows (PowerShell)
dir $HOME\AddressBookCache\
```

---

## Testing

### Run All Tests
```bash
    python -m unittest discover -s tests
```

### Run Specific Tests
```bash
python -m unittest tests.models.test_address_book
python -m unittest tests.models.test_birthday
python -m unittest tests.models.test_note
```

### Test Coverage
- Contact CRUD operations
- Phone validation
- Birthday calculations
- Note management with tags
- Search functionality
- Data persistence

---

## Project Structure

```
goit-personal-helper-team-project/
├── main.py                          # Entry point
├── README.md                        # Documentation
├── requirements.txt                 # Dependencies
├── src/
│   ├── bot_assistant.py            # Main bot logic
│   ├── constants/
│   │   └── constants.py            # Date formats
│   ├── decorators/
│   │   └── input_error.py          # Error handling
│   ├── models/
│   │   ├── address_book.py         # AddressBook class
│   │   ├── record.py               # Contact record
│   │   ├── field.py                # Base field
│   │   ├── name.py                 # Name field
│   │   ├── phone.py                # Phone with validation
│   │   ├── birthday.py             # Birthday field
│   │   ├── note.py                 # Note class
│   │   └── tag.py                  # Tag class
│   └── services/
│       └── absolute_path_provider.py
└── tests/
    └── models/
        ├── test_address_book.py
        ├── test_birthday.py
        └── test_note.py
```

---

## Troubleshooting

### Common Issues

**"Contact not found"**
- Check exact spelling and capitalization
- Use `all` to list all contacts

**Invalid phone format**
```
>>> add John 123-456-7890  # ❌ Wrong
>>> add John 1234567890    # ✓ Correct (10 digits)
```

**Invalid date format**
```
>>> add_birthday John 03/15/1990  # ❌ Wrong
>>> add_birthday John 15.03.1990  # ✓ Correct (DD.MM.YYYY)
```

**Note ID not found**
- Use `find <name>` to view note IDs
- Note IDs start at 1 and increment

**Data corrupted**
```bash
rm ~/AddressBookCache/address_book.pkl
python main.py  # Creates fresh database
```

**Command not recognized**
- Type `help` to see all commands
- Check command spelling

---

## Requirements

### System
- Python 3.10+
- OS: Windows, macOS, Linux

### Dependencies
Standard library only:
- `pickle` - Serialization
- `cmd` - CLI interface
- `datetime` - Date handling
- `re` - Regex
- `collections.UserDict` - Base class

No external packages required!

---

## Tips & Best Practices

1. **Descriptive names:** Use clear, searchable contact names
2. **Consistent tags:** Use standard tags like "work", "personal", "urgent"
3. **Regular backups:** Backup `~/AddressBookCache/address_book.pkl` periodically
4. **Use search:** Partial matches work for quick lookup
5. **Weekend handling:** Bot auto-adjusts weekend birthdays

---

### Development
1. Fork repository
2. Create feature branch: `git checkout -b feature-name`
3. Make changes
4. Run tests: `python -m unittest discover -s tests`
5. Commit: `git commit -am 'Add feature'`
6. Push: `git push origin feature-name`
7. Submit pull request

---

## Support

1. Check this README
2. Use `help` command
3. Review test files
4. See Troubleshooting section

---

**Version:** 1.0  
**Last Updated:** November 2025

Happy organizing with Jarvis! 🤖

---

Test covarage:
    [![Coverage](https://codecov.io/gh/nazarmyua/goit-personal-helper-team-project/branch/main/graph/badge.svg)](https://codecov.io/gh/nazarmyua/goit-personal-helper-team-project)
To run unit tests use:
    python -m unittest discover -s tests
