import shutil
import tempfile

import os


class DirectoryAndFileMixin(object):
    def setUp(self):
        self.temporary_directory = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.temporary_directory)

    def make_directory(self, pathlist):
        full_path = os.path.join(self.temporary_directory, *pathlist)
        if not os.path.exists(full_path):
            os.makedirs(full_path)
        return full_path

    def make_file(self, pathlist, content=''):
        self.make_directory(pathlist[:-1])
        full_path = os.path.join(self.temporary_directory, *pathlist)
        with open(full_path, 'w') as f:
            f.write(content)
        return full_path
