import unittest

from src.models.record import Record


class TestAddNote(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")

    def test_add_single_note(self):
        self.record.add_note("first note")
        self.assertIn(1, self.record.notes)
        self.assertEqual(self.record.notes[1].value, "first note")

    def test_add_multiple_notes_with_incrementing_ids(self):
        self.record.add_note("note one")
        self.record.add_note("note two")
        self.record.add_note("note three")

        self.assertEqual(self.record.notes[1].value, "note one")
        self.assertEqual(self.record.notes[2].value, "note two")
        self.assertEqual(self.record.notes[3].value, "note three")

    def test_add_note_strips_whitespace(self):
        self.record.add_note("   spaced note   ")
        self.assertEqual(self.record.notes[1].value, "spaced note")

    def test_add_empty_note_raises(self):
        with self.assertRaises(ValueError):
            self.record.add_note("")

    def test_add_whitespace_only_note_raises(self):
        with self.assertRaises(ValueError):
            self.record.add_note("    ")

    def test_add_note_with_special_characters(self):
        self.record.add_note("hello !@#$%^&*()")
        self.assertEqual(self.record.notes[1].value, "hello !@#$%^&*()")


class TestEditNote(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")
        self.record.add_note("first")
        self.record.add_note("second")
        self.record.add_note("third")

    def test_edit_note_success(self):
        self.record.edit_note(2, "updated second")
        self.assertEqual(self.record.notes[2].value, "updated second")

    def test_edit_note_strips_whitespace(self):
        self.record.edit_note(1, "   updated text   ")
        self.assertEqual(self.record.notes[1].value, "updated text")

    def test_edit_note_invalid_id_raises_keyerror(self):
        with self.assertRaises(KeyError):
            self.record.edit_note(999, "doesn't matter")

    def test_edit_note_empty_raises(self):
        with self.assertRaises(ValueError):
            self.record.edit_note(1, "")

    def test_edit_note_whitespace_only_raises(self):
        with self.assertRaises(ValueError):
            self.record.edit_note(1, "   ")

    def test_edit_note_replaces_entire_note_object(self):
        old_note_obj = self.record.notes[1]
        self.record.edit_note(1, "new text")
        new_note_obj = self.record.notes[1]

        self.assertIsNot(old_note_obj, new_note_obj)
        self.assertEqual(new_note_obj.value, "new text")

    def test_edit_note_with_special_characters(self):
        self.record.edit_note(3, "!@#$% updated")
        self.assertEqual(self.record.notes[3].value, "!@#$% updated")


class TestRemoveNote(unittest.TestCase):
    def setUp(self):
        self.record = Record("John")
        self.record.add_note("first")
        self.record.add_note("second")
        self.record.add_note("third")

    def test_remove_note_success(self):
        self.record.remove_note(2)
        self.assertNotIn(2, self.record.notes)

    def test_remove_note_reduces_count(self):
        initial_count = len(self.record.notes)
        self.record.remove_note(1)
        self.assertEqual(len(self.record.notes), initial_count - 1)

    def test_remove_note_invalid_id_raises_keyerror(self):
        with self.assertRaises(KeyError):
            self.record.remove_note(999)

    def test_remove_note_only_target_removed(self):
        self.record.remove_note(2)
        self.assertIn(1, self.record.notes)
        self.assertIn(3, self.record.notes)

    def test_remove_all_notes_one_by_one(self):
        self.record.remove_note(1)
        self.record.remove_note(2)
        self.record.remove_note(3)
        self.assertEqual(len(self.record.notes), 0)
