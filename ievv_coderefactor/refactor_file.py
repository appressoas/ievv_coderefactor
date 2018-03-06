import difflib

import sys

import os

from ievv_coderefactor import colorize


class RefactorFile(object):
    def __init__(self, root_directory, filepath, replacers):
        self.root_directory = root_directory
        self.filepath = filepath
        self.replacers = replacers
        with open(self.absolute_filepath, 'rb') as f:
            self.original_filecontent = f.read().decode('utf-8')
        self.new_filecontent = self._refactor_to_string()

    @property
    def absolute_filepath(self):
        return os.path.join(self.root_directory, self.filepath)

    def did_update(self):
        return self.original_filecontent != self.new_filecontent

    def _refactor_to_string(self):
        new_string = self.original_filecontent
        for replacer in self.replacers:
            new_string = replacer.replace(new_string)
        return new_string

    def refactor(self):
        with open(self.absolute_filepath, 'wb') as f:
            f.write(self.new_filecontent.encode('utf-8'))

    def iter_difflines(self):
        difflist = list(difflib.Differ().compare(
            self.original_filecontent.splitlines(keepends=True),
            self.new_filecontent.splitlines(keepends=True)))
        for diffline in difflist:
            if diffline.startswith(' '):
                continue
            yield diffline

    def print_diff(self):
        if not self.did_update():
            return
        print(colorize.colored_text('{}:'.format(self.filepath), colorize.COLOR_BLUE, bold=True))
        for diffline in self.iter_difflines():
            if diffline.startswith('+'):
                color = colorize.COLOR_GREEN
            elif diffline.startswith('-'):
                color = colorize.COLOR_RED
            else:
                color = colorize.COLOR_GREY
            sys.stdout.write(colorize.colored_text(diffline, color))
