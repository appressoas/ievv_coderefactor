import json
import os

import fire

from ievv_coderefactor import colorize
from ievv_coderefactor.refactor_tree import RefactorTree
from ievv_coderefactor.refactorlogger import RefactorLogger
from ievv_coderefactor.strip_json_comments import strip_json_comments


class Cli(object):
    """
    Migrate a codebase from JSON config file.
    """
    def refactor(self, directory, config, pretend=False, stdout_loglevel='summary',
                 plain_logfile_path=None):
        refactor_tree = RefactorTree(root_directory=os.path.abspath(directory))
        with open(config, 'r') as configfile:
            configjson = configfile.read()
        configjson = strip_json_comments(configjson)

        if stdout_loglevel == 'none':
            stdout_loglevel = None
        logger = RefactorLogger(stdout_loglevel=stdout_loglevel,
                                plain_logfile_path=plain_logfile_path,
                                pretend=pretend)
        refactor_tree.configure_from_dict(config_dict=json.loads(configjson))
        if pretend:
            logger.log_message('Starting in pretend mode. Printing what we would do, not changing anything on disk.')
            logger.log_message('WARNING: Renaming of directories and files is not always '
                               'shown correctly in pretend mode since renames may depend on '
                               'previous renames to be correct.', color=colorize.COLOR_YELLOW, bold=True)
        else:
            logger.log_message('Starting refactoring.')
        refactor_tree.refactor(pretend=pretend, logger=logger)
        logger.log_message('Refactoring DONE', color=colorize.COLOR_GREEN)


def main():
    fire.Fire(Cli)


if __name__ == '__main__':
    main()
