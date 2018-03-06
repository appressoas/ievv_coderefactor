import os


class FileOrDirectoryRenamer(object):
    """
    File or directory renamer.
    """
    def __init__(self, root_directory, path, replacers):
        """

        Args:
            root_directory (str): The root directory path.
            path (str): The path relative to the root directory.
            replacers (list): List/iterable of :class:`ievv_coderefactor.replacers.AbstractReplacer`
                objects.
        """
        self.root_directory = os.path.normpath(root_directory)
        self.original_path = path
        if not self.original_path.startswith('/'):
            self.original_path = '/{}'.format(self.original_path)
        self.replacers = replacers
        self.new_path = self._make_new_path()

    def did_update(self):
        return self.original_path != self.new_path

    def _make_new_path(self):
        new_path = self.original_path
        for replacer in self.replacers:
            new_path = replacer.replace(new_path)
        return new_path

    def _make_absolute_path(self, path):
        if path.startswith('/'):
            path = path.lstrip('/')
        return os.path.join(self.root_directory, os.path.normpath(path))

    @property
    def original_absolute_path(self):
        return self._make_absolute_path(self.original_path)

    @property
    def new_absolute_path(self):
        return self._make_absolute_path(self.new_path)

    @property
    def is_directory(self):
        return os.path.isdir(self.original_path)

    def rename(self):
        """
        Rename the file/directory.

        Handles missing parent directories.
        """
        new_parent_directory = os.path.dirname(self.new_absolute_path)
        if not os.path.exists(new_parent_directory):
            os.makedirs(new_parent_directory)
        os.rename(self.original_absolute_path, self.new_absolute_path)
