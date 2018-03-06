import fnmatch
import os

import fire


class Cli(object):
    """
    Migrate a codebase from JSON config file.
    """
    def _make_exclude_directories(self, extra_exclude_directories):
        exclude_directories = [
            '**/node_modules',
            '.git',
            '**/.git',
        ]
        exclude_directories.extend(extra_exclude_directories)
        return exclude_directories

    def _fnmatch_many(self, path, patterns):
        for pattern in patterns:
            if fnmatch.fnmatch(path, pattern):
                return True
        return False

    def __iter_walk_directory(self, toplevel_directory,
                              filepatterns,
                              include_files=False,
                              include_directories=False,
                              exclude_directories=tuple()):
        exclude_directories = self._make_exclude_directories(exclude_directories)

        for directory, subdirectories, filenames in os.walk(toplevel_directory):
            for subdirectory in subdirectories:
                subdirectorypath = os.path.join(directory, subdirectory)
                if self._fnmatch_many(subdirectorypath, exclude_directories):
                    subdirectories.remove(subdirectory)
                elif include_directories:
                    yield subdirectorypath
            if include_files:
                for filename in filenames:
                    filepath = os.path.join(directory, filename)
                    if os.path.islink(filepath):
                        continue
                    if self._fnmatch_many(filepath, filepatterns):
                        yield filepath
    #
    # def _refactor_python_file(self, filepath, verbose=False, pretend=False):
    #     refactor = RefactorPythonFile(filepath=filepath)
    #     if verbose:
    #         refactor.print_diff()

    # def refactor_python_code(self, directory, exclude_directories=tuple(), verbose=False, pretend=False):
    #     """
    #     Refactor .py files.
    #
    #     --directory
    #         The directory to refactory. Typically the root module directory
    #         for the project that uses django_cradmin 1x.
    #     --exclude-directories
    #         Add extra fnmatch/glob exclude patterns for directories.
    #         The default exclude patterns are ['**/node_modules', '.git', '**/.git'].
    #
    #         Example: ``--exclude-directories "('libs/*', 'extrastuff/*')"``.
    #
    #         We do not follow symlinks when refactoring, so you do not
    #         have to exclude symlinked directories.
    #     """
    #     for filepath in self.__iter_walk_directory(
    #             toplevel_directory=directory,
    #             filepatterns=['*.py'],
    #             include_files=True,
    #             exclude_directories=exclude_directories):
    #         pass
    #         # self._refactor_python_file(filepath=filepath, verbose=verbose)
    #
    # def refactor_rst_code(self, directory, exclude_directories=tuple(), verbose=False, pretend=False):
    #     """
    #     Refactor .rst files.
    #
    #     --directory
    #         The directory to refactory. Typically the root module directory
    #         for the project that uses django_cradmin 1x.
    #     --exclude-directories
    #         Add extra fnmatch/glob exclude patterns for directories.
    #         The default exclude patterns are ['**/node_modules', '.git', '**/.git'].
    #
    #         Example: ``--exclude-directories "('libs/*', 'extrastuff/*')"``.
    #
    #         We do not follow symlinks when refactoring, so you do not
    #         have to exclude symlinked directories.
    #     """
    #     for filepath in self.__iter_walk_directory(
    #             toplevel_directory=directory,
    #             filepatterns=['*.rst'],
    #             include_files=True,
    #             exclude_directories=exclude_directories):
    #         self._refactor_python_file(filepath=filepath, verbose=verbose,
    #                                    pretend=False)
    #
    # def refactor_all(self, directory, exclude_directories=tuple(), verbose=False, pretend=False):
    #     self.refactor_python_code(directory=directory, exclude_directories=exclude_directories,
    #                               verbose=verbose, pretend=pretend)
    #     self.refactor_rst_code(directory=directory, exclude_directories=exclude_directories,
    #                            verbose=verbose, pretend=pretend)

    def refactor(self, directory, config_json, verbose=False):
        pass

    def refactor_pretend(self, directory, config_json):
        pass


def main():
    fire.Fire(Cli)


if __name__ == '__main__':
    main()
