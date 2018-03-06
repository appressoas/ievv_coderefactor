from unittest import TestCase

from ievv_coderefactor.strip_json_comments import strip_json_comments


class TestStripJsonComments(TestCase):
    def test_first_in_line(self):
        self.assertEqual(
            strip_json_comments('//Hello'),
            '')

    def test_indented(self):
        self.assertEqual(
            strip_json_comments('    //Hello'),
            '')

    def test_full(self):
        self.assertEqual(
            strip_json_comments('// Comment 1\n{\n//Comment 2\n  "x": 10\n}'),
            '{\n  "x": 10\n}')
