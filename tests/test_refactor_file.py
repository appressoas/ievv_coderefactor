from unittest import TestCase

from ievv_coderefactor.refactor_file import RefactorFile
from ievv_coderefactor.replacers import RegexReplacer
from tests.directory_and_file_mixin import DirectoryAndFileMixin


class TestRefactorFile(DirectoryAndFileMixin, TestCase):
    def test_simple(self):
        filepath = self.make_file(['test.py'], 'from oldstuff import MyOldClass')
        filerefactor = RefactorFile(filepath=filepath, replacers=[
            RegexReplacer(r'from\s+oldstuff\s+import',
                          r'from newstuff import'),
            RegexReplacer(r'MyOldClass',
                          'MyNewClass'),
        ])
        self.assertEqual(filerefactor.new_filecontent, 'from newstuff import MyNewClass')
        filerefactor.refactor()
        self.assertEqual(open(filepath).read(), 'from newstuff import MyNewClass')
