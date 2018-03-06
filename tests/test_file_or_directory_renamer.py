import os
from unittest import TestCase

from ievv_coderefactor.file_or_directory_renamer import FileOrDirectoryRenamer
from ievv_coderefactor.replacer_registry import RegexReplacer
from tests.directory_and_file_mixin import DirectoryAndFileMixin


class TestFileOrDirectoryRenamer(DirectoryAndFileMixin, TestCase):
    def test_rename_directory_sanity(self):
        directory_absolute_path = self.make_directory(['my', 'old', 'directory'])
        filerenamer = FileOrDirectoryRenamer(
            root_directory=self.temporary_directory,
            path=os.path.join('my', 'old'),
            replacers=[
                RegexReplacer(r'^/my/old$', '/my/new'),
            ])
        self.assertEqual(filerenamer.original_absolute_path,
                         os.path.join(self.temporary_directory, 'my', 'old'))
        self.assertEqual(filerenamer.new_absolute_path,
                         os.path.join(self.temporary_directory, 'my', 'new'))
        filerenamer.rename()
        self.assertFalse(os.path.exists(directory_absolute_path))
        self.assertTrue(os.path.exists(filerenamer.new_absolute_path))
        self.assertTrue(os.path.exists(os.path.join(self.temporary_directory, 'my', 'new', 'directory')))

    def test_rename_file_sanity(self):
        filepath = ['my', 'old', 'test.py']
        file_absolute_path = self.make_file(filepath, '')
        filerenamer = FileOrDirectoryRenamer(
            root_directory=self.temporary_directory,
            path=os.path.join(*filepath),
            replacers=[
                RegexReplacer(r'^/my/old/test.py$', '/my/new/supertest.py'),
            ])
        self.assertEqual(filerenamer.original_absolute_path,
                         os.path.join(self.temporary_directory, 'my', 'old', 'test.py'))
        self.assertEqual(filerenamer.new_absolute_path,
                         os.path.join(self.temporary_directory, 'my', 'new', 'supertest.py'))
        filerenamer.rename()
        self.assertFalse(os.path.exists(file_absolute_path))
        self.assertTrue(os.path.exists(filerenamer.new_absolute_path))
