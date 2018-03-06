import fnmatch

import os


class DirectoryTreeWalker(object):
    def __fnmatch_many(self, path, patterns):
        if not patterns:
            return False
        for pattern in patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
        return False

    def get_root_directory(self):
        raise NotImplementedError()

    def get_exclude_directories(self):
        raise NotImplementedError()

    def get_filepatterns(self):
        return []

    def __iter_walk_directory(self, include_files=False, include_directories=False):
        exclude_directories = self.get_exclude_directories()
        for directory, subdirectories, filenames in os.walk(self.get_root_directory()):
            for subdirectory in subdirectories:
                subdirectorypath = os.path.join(directory, subdirectory)
                if self.__fnmatch_many(subdirectorypath, exclude_directories):
                    subdirectories.remove(subdirectory)
                elif include_directories:
                    yield os.path.relpath(subdirectorypath, self.get_root_directory())
            if include_files:
                for filename in filenames:
                    filepath = os.path.join(directory, filename)
                    if os.path.islink(filepath):
                        continue
                    if self.__fnmatch_many(filepath, self.get_filepatterns()):
                        yield os.path.relpath(filepath, self.get_root_directory())

    def iter_walk_directories(self):
        return self.__iter_walk_directory(
            include_directories=True,
            include_files=False)

    def iter_walk_files(self):
        return self.__iter_walk_directory(
            include_directories=False,
            include_files=True)
