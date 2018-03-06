from unittest import TestCase

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
                    "replacers": [
                        {
                            "replacer": "RegexReplacer",
                            "pattern": "from\\s+oldstuff\\s+import",
                            "replacement": "from newstuff import"
                        },
                        {
                            "replacer": "RegexReplacer",
                            "pattern": "MyOldClass",
                            "replacement": "MyNewClass"
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
