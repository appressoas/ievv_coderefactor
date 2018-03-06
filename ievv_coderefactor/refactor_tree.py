from ievv_coderefactor import replacer_registry
from ievv_coderefactor.directorytreewalker import DirectoryTreeWalker
from ievv_coderefactor.file_or_directory_renamer import FileOrDirectoryRenamer
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


class RenameFilesOrDirectories(DirectoryTreeWalker):
    @classmethod
    def make_kwargs_from_raw_replacer_list(cls, raw_renamers_list):
        replacers = []
        for renamer_config in raw_renamers_list:
            renamer_kwargs = dict(renamer_config)
            replacer_name = renamer_kwargs.pop('replacer')
            replacer_class = replacer_registry.REPLACER_REGISTRY[replacer_name]
            replacer = replacer_class(**renamer_kwargs)
            replacers.append(replacer)
        return dict(replacers=replacers)

    def __init__(self, root_directory, exclude_directories, replacers):
        self.root_directory = root_directory
        self.exclude_directories = exclude_directories
        self.replacers = replacers

    def get_root_directory(self):
        return self.root_directory

    def get_exclude_directories(self):
        return self.exclude_directories

    def rename(self, pretend=False, logger=None):
        for path in self.iter_walk_files_and_directories():
            renamer = FileOrDirectoryRenamer(
                root_directory=self.root_directory,
                path=path,
                replacers=self.replacers)
            if logger:
                logger.log(renamer)
            if not pretend:
                renamer.rename()


class RefactorTree(object):
    def __init__(self, root_directory):
        self.root_directory = root_directory
        self.exclude_directories = {
            ".git",
            "**/.git"
        }
        self.refactor_files_objects = []
        self.rename_files_or_directories_objects = []

    def configure_from_dict(self, config_dict):
        self.add_exclude_directories(config_dict.get('extra_exclude_directories', []))
        for refactor_file_config in config_dict.get('refactor_files', []):
            self.add_refactor_files(
                **RefactorFiles.make_kwargs_from_dict(
                    config_dict=refactor_file_config
                ))
        raw_renamer_lists = config_dict.get('rename', [])
        for raw_renamer_list in raw_renamer_lists:
            self.add_files_and_directories_rename(
                **RenameFilesOrDirectories.make_kwargs_from_raw_replacer_list(raw_renamer_list)
            )

    def add_refactor_files(self, **refactor_files_kwargs):
        """
        Add :class:`ievv_coderefactor.refactor_tree.RefactorFiles`.

        Args:
            **refactor_files_kwargs: kwargs for :class:`ievv_coderefactor.refactor_tree.RefactorFiles`.
                Do not include ``root_directory`` or ``exclude_directories`` - they are added
                automatically.
        """
        self.refactor_files_objects.append(
            RefactorFiles(
                root_directory=self.root_directory,
                exclude_directories=self.exclude_directories,
                **refactor_files_kwargs)
        )

    def add_files_and_directories_rename(self, **kwargs):
        """
        Configure rename of files and directories.

        Args:
            **kwargs: kwargs for :class:`ievv_coderefactor.refactor_tree.RenameFilesOrDirectories`.
                Do not include ``root_directory`` or ``exclude_directories`` - they are added
                automatically.
        """
        self.rename_files_or_directories_objects.append(
            RenameFilesOrDirectories(
                root_directory=self.root_directory,
                exclude_directories=self.exclude_directories,
                **kwargs
            )
        )

    def add_exclude_directories(self, *exclude_directories):
        self.exclude_directories.update(*exclude_directories)

    def refactor(self, pretend=False, logger=None):
        for refactor_files_object in self.refactor_files_objects:
            refactor_files_object.refactor(pretend=pretend, logger=logger)
        for rename_files_or_directories_object in self.rename_files_or_directories_objects:
            rename_files_or_directories_object.rename(pretend=pretend, logger=logger)
