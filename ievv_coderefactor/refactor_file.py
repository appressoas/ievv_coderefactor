import difflib

import sys

from ievv_coderefactor import colorize


class RefactorFile(object):
    def __init__(self, filepath, renamers):
        self.filepath = filepath
        self.renamers = renamers
        self.original_filecontent = open(self.filepath, 'rb').read().decode('utf-8')
        self.new_filecontent = self._refactor_to_string()

    def did_update(self):
        return self.original_filecontent != self.new_filecontent

    def _refactor_to_string(self):
        new_string = self.original_filecontent
        for replacer in self.renamers:
            new_string = replacer.replace(new_string)
        return new_string

    def refactor(self):
        with open(self.filepath, 'wb') as f:
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
