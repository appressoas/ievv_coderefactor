import fnmatch

import os

import re


class DirectoryTreeWalker(object):
    def __regexmatch_many(self, path, patterns):
        if patterns is None:
            return True
        for pattern in patterns:
            isolated_path = '/{}'.format(path)
            if re.match(pattern, isolated_path):
                return True
        return False

    def get_root_directory(self):
        raise NotImplementedError()

    def get_exclude_directories(self):
        raise NotImplementedError()

    def get_exclude_files(self):
        raise NotImplementedError()

    def get_filepatterns(self):
        return None

    def __iter_walk_directory(self, include_files=False, include_directories=False):
        exclude_directories = self.get_exclude_directories()
        for directory, subdirectories, filenames in os.walk(self.get_root_directory()):
            for subdirectory in subdirectories:
                subdirectorypath = os.path.join(directory, subdirectory)
                relative_subdirectorypath = os.path.relpath(subdirectorypath, self.get_root_directory())
                if self.__regexmatch_many(relative_subdirectorypath, exclude_directories):
                    subdirectories.remove(subdirectory)
                elif include_directories:
                    yield relative_subdirectorypath
            if include_files:
                for filename in filenames:
                    filepath = os.path.join(directory, filename)
                    if os.path.islink(filepath):
                        continue
                    relative_filepath = os.path.relpath(filepath, self.get_root_directory())
                    if self.__regexmatch_many(relative_filepath, self.get_exclude_files()):
                        continue
                    if self.__regexmatch_many(relative_filepath, self.get_filepatterns()):
                        yield relative_filepath

    def iter_walk_files_and_directories(self):
        return self.__iter_walk_directory(
            include_directories=True,
            include_files=True)

    def iter_walk_files(self):
        return self.__iter_walk_directory(
            include_directories=False,
            include_files=True)
