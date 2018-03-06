from unittest import TestCase

from ievv_coderefactor.replacers import RegexReplacer, StringReplacer


class TestStringReplacer(TestCase):
    def test_simple(self):
        self.assertEqual(
            StringReplacer(r'test', 'test2').replace('This is a test!'),
            'This is a test2!')

    def test_multiple_replacements(self):
        self.assertEqual(
            StringReplacer(r'test', 'test2').replace('My supertest test testing!'),
            'My supertest2 test2 test2ing!')


class TestRegexReplacer(TestCase):
    def test_simple(self):
        self.assertEqual(
            RegexReplacer(r'test', 'test2').replace('This is a test!'),
            'This is a test2!')

    def test_advanced(self):
        replacer = RegexReplacer(r'from\s+mymodule\.my_(old|veryold)_file(.*?)$',
                                 r'from mymodule.my_new_file\2')
        self.assertEqual(
            replacer.replace('This is a test!'),
            'This is a test!')
        self.assertEqual(
            replacer.replace('from mymodule.my_old_file import MyClass\ntest'),
            'from mymodule.my_new_file import MyClass\ntest')
        self.assertEqual(
            replacer.replace('from mymodule.my_veryold_file import MyClass\ntest'),
            'from mymodule.my_new_file import MyClass\ntest')

    def test_multiple_replacements(self):
        self.assertEqual(
            RegexReplacer(r'test', 'test2').replace('My supertest test testing!'),
            'My supertest2 test2 test2ing!')
