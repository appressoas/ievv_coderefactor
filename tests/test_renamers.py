from unittest import TestCase

from ievv_coderefactor.renamers import RegexRenamer, StringRenamer


class TestStringRenamer(TestCase):
    def test_simple(self):
        self.assertEqual(
            StringRenamer(r'test', 'test2').replace('This is a test!'),
            'This is a test2!')

    def test_multiple_replacements(self):
        self.assertEqual(
            StringRenamer(r'test', 'test2').replace('My supertest test testing!'),
            'My supertest2 test2 test2ing!')


class TestRegexRenamer(TestCase):
    def test_simple(self):
        self.assertEqual(
            RegexRenamer(r'test', 'test2').replace('This is a test!'),
            'This is a test2!')

    def test_advanced(self):
        renamer = RegexRenamer(r'from\s+mymodule\.my_(old|veryold)_file(.*?)$',
                               r'from mymodule.my_new_file\2')
        self.assertEqual(
            renamer.replace('This is a test!'),
            'This is a test!')
        self.assertEqual(
            renamer.replace('from mymodule.my_old_file import MyClass\ntest'),
            'from mymodule.my_new_file import MyClass\ntest')
        self.assertEqual(
            renamer.replace('from mymodule.my_veryold_file import MyClass\ntest'),
            'from mymodule.my_new_file import MyClass\ntest')

    def test_multiple_replacements(self):
        self.assertEqual(
            RegexRenamer(r'test', 'test2').replace('My supertest test testing!'),
            'My supertest2 test2 test2ing!')
