import unittest
from src.models.note import Note


class TestNote(unittest.TestCase):
    def test_valid_note(self):
        note = Note("This is a valid note")
        self.assertEqual(note.value, "This is a valid note")

    def test_note_strips_whitespace(self):
        note = Note("  note with spaces  ")
        self.assertEqual(note.value, "note with spaces")

    def test_empty_note_raises_error(self):
        with self.assertRaises(ValueError):
            Note("")

    def test_whitespace_only_note_raises_error(self):
        with self.assertRaises(ValueError):
            Note("   ")

    def test_note_with_tabs_and_newlines_raises_error(self):
        with self.assertRaises(ValueError):
            Note("\t\n")

    def test_note_value_setter_strips_whitespace(self):
        note = Note("initial note")
        note.value = "  updated note  "
        self.assertEqual(note.value, "updated note")

    def test_note_value_setter_empty_raises_error(self):
        note = Note("initial note")
        with self.assertRaises(ValueError):
            note.value = ""

    def test_note_with_special_characters(self):
        note = Note("Note with special chars: !@#$%^&*()")
        self.assertEqual(note.value, "Note with special chars: !@#$%^&*()")


if __name__ == "__main__":
    unittest.main()
