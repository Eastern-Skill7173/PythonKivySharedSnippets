"""
Module is incomplete and NOT tested
"""

from typing import List
from kivy.utils import platform
from plyer import filechooser
from src.constants.platform_directorties import HOME_DIRECTORY
from kivymd.uix.filemanager import MDFileManager

__all__ = (
    "FileChooser",
)


class FileChooser:
    """Custom file chooser to open the proper dialog on different platforms."""
    _in_app_file_chooser = None

    @classmethod
    def _check_in_app_file_chooser(cls) -> None:
        """Checker function to avoid:
            `
            ValueError: KivyMD: App object must be initialized
            before loading root widget. See:
            https://github.com/kivymd/KivyMD/wiki/Modules-Material-App#exceptions
            `
        """
        if not cls._in_app_file_chooser:
            cls._in_app_file_chooser = MDFileManager(
                select_path=lambda: None
            )

    @classmethod
    def choose_dir(cls, *args, **kwargs) -> List[str]:
        if platform not in ("android", "ios"):
            return filechooser.choose_dir(*args, **kwargs)
        else:
            cls._check_in_app_file_chooser()
            cls._in_app_file_chooser.selector = "folder"
            cls._in_app_file_chooser.show(HOME_DIRECTORY)

    @classmethod
    def open_file(cls, *args, **kwargs) -> List[str]:
        if platform != "ios":
            return filechooser.open_file(*args, **kwargs)
        else:
            cls._check_in_app_file_chooser()
            cls._in_app_file_chooser.selector = "file"
            cls._in_app_file_chooser.show(HOME_DIRECTORY)

    @classmethod
    def save_file(cls, *args, **kwargs) -> List[str]:
        if platform != "ios":
            return filechooser.save_file(*args, **kwargs)
        else:
            cls._check_in_app_file_chooser()
            cls._in_app_file_chooser.selector = "folder"
            cls._in_app_file_chooser.show(HOME_DIRECTORY)
