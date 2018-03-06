from unittest import TestCase

import os

from ievv_coderefactor.refactor_tree import RefactorTree
from tests.directory_and_file_mixin import DirectoryAndFileMixin


class TestRefactorTree(DirectoryAndFileMixin, TestCase):
    def test_configure_from_dict__refactor_files(self):
        absolute_filepath = self.make_file(['test.py'], 'from oldstuff import MyOldClass')
        treerefactor = RefactorTree(
            root_directory=self.temporary_directory)
        treerefactor.configure_from_dict({
            'refactor_files': [
                {
                    'filepatterns': ['*.py'],
                    'replacers': [
                        {
                            'replacer': 'RegexReplacer',
                            'pattern': 'from\\s+oldstuff\\s+import',
                            'replacement': 'from newstuff import'
                        },
                        {
                            'replacer': 'RegexReplacer',
                            'pattern': 'MyOldClass',
                            'replacement': 'MyNewClass'
                        }
                    ]
                }
            ]
        })
        self.assertEqual(len(treerefactor.refactor_files_objects), 1)
        self.assertEqual(treerefactor.refactor_files_objects[0].root_directory,
                         self.temporary_directory)
        self.assertEqual(treerefactor.refactor_files_objects[0].exclude_directories,
                         treerefactor.exclude_directories)
        self.assertEqual(len(treerefactor.refactor_files_objects[0].replacers),
                         2)
        treerefactor.refactor()
        with open(absolute_filepath) as f:
            self.assertEqual(f.read(), 'from newstuff import MyNewClass')

    def test_configure_from_dict__rename(self):
        self.make_file(['my', 'old', 'test.py'])
        self.make_file(['my', 'old', 'test2.py'])
        treerefactor = RefactorTree(
            root_directory=self.temporary_directory)
        treerefactor.configure_from_dict({
            'rename': [
                [
                    {
                        'replacer': 'RegexReplacer',
                        'pattern': '^my/old/test.py$',
                        'replacement': 'my/supernew/test.py'
                    },
                ],
                [
                    {
                        'replacer': 'RegexReplacer',
                        'pattern': '^my/old$',
                        'replacement': 'my/new'
                    },
                ]
            ]
        })
        self.assertEqual(len(treerefactor.rename_files_or_directories_objects), 2)
        self.assertEqual(treerefactor.rename_files_or_directories_objects[0].root_directory,
                         self.temporary_directory)
        self.assertEqual(treerefactor.rename_files_or_directories_objects[0].exclude_directories,
                         treerefactor.exclude_directories)
        treerefactor.refactor()
        self.assertFalse(os.path.exists(os.path.join(self.temporary_directory, 'my', 'old', 'test.py')))
        self.assertFalse(os.path.exists(os.path.join(self.temporary_directory, 'my', 'old', 'test2.py')))
        self.assertTrue(os.path.exists(os.path.join(self.temporary_directory, 'my', 'supernew', 'test.py')))
        self.assertTrue(os.path.exists(os.path.join(self.temporary_directory, 'my', 'new', 'test2.py')))
