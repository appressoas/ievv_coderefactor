from ievv_coderefactor import replacer_registry
from ievv_coderefactor.directorytreewalker import DirectoryTreeWalker
from ievv_coderefactor.refactor_file import RefactorFile


class RefactorFiles(DirectoryTreeWalker):
    @classmethod
    def make_kwargs_from_dict(cls, config_dict):
        filepatterns = config_dict['filepatterns']
        replacers = []
        for replacer_config in config_dict['replacers']:
            replacer_kwargs = dict(replacer_config)
            replacer_name = replacer_kwargs.pop('replacer')
            replacer_class = replacer_registry.REPLACER_REGISTRY[replacer_name]
            replacer = replacer_class(**replacer_kwargs)
            replacers.append(replacer)
        return dict(filepatterns=filepatterns,
                    replacers=replacers)

    def __init__(self, root_directory, exclude_directories, filepatterns, replacers):
        self.root_directory = root_directory
        self.exclude_directories = exclude_directories
        self.filepatterns = filepatterns
        self.replacers = replacers

    def get_root_directory(self):
        return self.root_directory

    def get_exclude_directories(self):
        return self.exclude_directories

    def get_filepatterns(self):
        return self.filepatterns

    def refactor(self, pretend=False, logger=None):
        for filepath in self.iter_walk_files():
            refactorer = RefactorFile(
                root_directory=self.root_directory,
                filepath=filepath,
                replacers=self.replacers)
            if logger:
                logger.log(refactorer)
            if not pretend:
                refactorer.refactor()


class RefactorTree(object):
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.exclude_directories = {
            ".git",
            "**/.git"
        }
        self.refactor_files_objects = []
        self.file_or_directory_renamer_objects = []

    def configure_from_dict(self, config_dict):
        self.add_exclude_directories(config_dict.get('extra_exclude_directories', []))
        for refactor_file_config in config_dict.get('refactor_files', []):
            self.add_refactor_files(
                **RefactorFiles.make_kwargs_from_dict(
                    config_dict=refactor_file_config
                ))

    def add_refactor_files(self, **refactor_files_kwargs):
        self.refactor_files_objects.append(
            RefactorFiles(
                root_directory=self.root_directory,
                exclude_directories=self.exclude_directories,
                **refactor_files_kwargs)
        )

    # def add_file_or_directory_renamers(self, *file_or_directory_renamer_kwargs_list):
    #     for kwargs in file_or_directory_renamer_kwargs_list:
    #         self.file_or_directory_renamer_objects.append(
    #             FileOrDirectoryRenamer(root_directory=self.root_directory,
    #                                    **kwargs)
    #         )

    def add_exclude_directories(self, *exclude_directories):
        self.exclude_directories.update(*exclude_directories)

    def refactor(self, pretend=False, logger=None):
        for refactor_files_object in self.refactor_files_objects:
            refactor_files_object.refactor(pretend=pretend, logger=logger)
