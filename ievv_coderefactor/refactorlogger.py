from __future__ import unicode_literals
from ievv_coderefactor import colorize


class RefactorLogger(object):
    STDOUT_LOGLEVEL_SUMMARY = 'summary'
    STDOUT_LOGLEVEL_ALL = 'all'

    def __init__(self, stdout_loglevel=None, plain_logfile_path=None,
                 pretend=False):
        self.stdout_loglevel = stdout_loglevel
        self.plain_logfile_path = plain_logfile_path
        self.plain_logfile = None
        self.pretend = pretend
        if plain_logfile_path:
            self.plain_logfile = open(plain_logfile_path, 'a')

    def _prefix_message(self, message):
        if self.pretend:
            return '[PRETEND] {}'.format(message)
        return message

    def _stdout_log(self, message):
        print(self._prefix_message(message))

    def _plain_logfile_log(self, message):
        if not self.plain_logfile_path:
            return
        self.plain_logfile.write(self._prefix_message('{}\n'.format(message)))

    def log_message(self, message, **colorize_kwargs):
        if self.stdout_loglevel is not None:
            if colorize_kwargs:
                self._stdout_log(colorize.colored_text(message, **colorize_kwargs))
            else:
                self._stdout_log(message)
        self._plain_logfile_log(message)

    def log_refactor_file(self, refactor_file):
        if not refactor_file.did_update():
            return
        if self.stdout_loglevel == self.STDOUT_LOGLEVEL_SUMMARY:
            self._stdout_log(
                message='{} {}'.format(
                    colorize.colored_text('[U]', color=colorize.COLOR_BLUE, bold=True),
                    refactor_file.filepath)
            )
        elif self.stdout_loglevel == self.STDOUT_LOGLEVEL_ALL:
            self._stdout_log(
                message='{} {} - DIFF:\n{}'.format(
                    colorize.colored_text('[UPDATE]', color=colorize.COLOR_BLUE, bold=True),
                    refactor_file.filepath,
                    refactor_file.get_formatted_diff(use_colors=True, indent='    ')
                )
            )
        self._plain_logfile_log(
            message='[UPDATE] {} - DIFF:\n{}'.format(
                refactor_file.filepath,
                refactor_file.get_formatted_diff(indent='    ')
            )
        )

    def log_rename_file_or_directory(self, file_or_directory_renamer):
        if not file_or_directory_renamer.did_update():
            return
        if self.stdout_loglevel == self.STDOUT_LOGLEVEL_SUMMARY:
            self._stdout_log(
                message='{} {} -> {}'.format(
                    colorize.colored_text('[R]', color=colorize.COLOR_BLUE, bold=True),
                    file_or_directory_renamer.original_path,
                    file_or_directory_renamer.new_path
                )
            )
        elif self.stdout_loglevel == self.STDOUT_LOGLEVEL_ALL:
            self._stdout_log(
                message='{} {} -> {}'.format(
                    colorize.colored_text('[RENAME]', color=colorize.COLOR_BLUE, bold=True),
                    file_or_directory_renamer.original_path,
                    file_or_directory_renamer.new_path
                )
            )
        self._plain_logfile_log(
            message='[RENAME] {} -> {}'.format(
                file_or_directory_renamer.original_path,
                file_or_directory_renamer.new_path
            )
        )
