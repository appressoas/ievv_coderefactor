import fnmatch
import json
import os

import fire

from ievv_coderefactor.refactor_tree import RefactorTree


class Cli(object):
    """
    Migrate a codebase from JSON config file.
    """
    def refactor(self, directory, config, pretend=False):
        refactor_tree = RefactorTree(root_directory=os.path.abspath(directory))
        with open(config, 'r') as configfile:
            configjson = configfile.read()
        refactor_tree.configure_from_dict(config_dict=json.loads(configjson))
        refactor_tree.refactor(pretend=pretend)


def main():
    fire.Fire(Cli)


if __name__ == '__main__':
    main()
