from unittest import TestCase

from ievv_coderefactor.refactor_file import RefactorFile
from ievv_coderefactor.replacer_registry import RegexReplacer
from tests.directory_and_file_mixin import DirectoryAndFileMixin


class TestRefactorFile(DirectoryAndFileMixin, TestCase):
    def test_simple(self):
        absolute_filepath = self.make_file(['test.py'], 'from oldstuff import MyOldClass')
        filerefactor = RefactorFile(
            root_directory=self.temporary_directory,
            filepath='test.py',
            replacers=[
                RegexReplacer(r'from\s+oldstuff\s+import',
                              r'from newstuff import'),
                RegexReplacer(r'MyOldClass',
                              'MyNewClass'),
            ])
        self.assertEqual(filerefactor.new_filecontent, 'from newstuff import MyNewClass')
        filerefactor.refactor()
        self.assertEqual(open(absolute_filepath).read(), 'from newstuff import MyNewClass')
