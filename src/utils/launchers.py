import os
import subprocess
import webbrowser
from src.constants import CURRENT_MACHINE
from src.type_aliases import FilePath
from src.utils import convert_file_path_to_string

__all__ = (
    "open_link",
    "open_terminal",
    "open_file",
    "open_file_explorer",
)


def open_link(link: str, new: int = 2, auto_raise: bool = True) -> None:
    """
    Convenience function to open the given url in user's default browser
    :param link: URL Address to be opened in user's default browser
    :param new: Where to open the link (in a new tab, existing tab or new page)
    :param auto_raise: Whether to raise the browser window or not
    :return: None
    """
    webbrowser.open(link, new=new, autoraise=auto_raise)


def open_terminal(directory: FilePath) -> None:
    """
    Convenience function to launch the terminal with the given directory
    :param directory: Directory to launch the terminal with
    :return: None
    """
    directory = convert_file_path_to_string(directory)
    subprocess.Popen(["cd", f'"{directory}"'])


def open_file(file_path: FilePath) -> None:
    """
    Convenience function to open the given file path with the default program
    across all `Linux`, `OSX`, `Windows`
    :param file_path: Path to the file to be opened
    :return: None
    """
    file_path = convert_file_path_to_string(file_path)
    if CURRENT_MACHINE == "Windows":
        os.startfile(file_path)
    elif CURRENT_MACHINE == "Darwin":
        subprocess.Popen(["open", file_path])
    else:
        subprocess.Popen(["xdg-open", file_path])


def open_file_explorer(
        file_or_directory_path: FilePath,
        highlight: bool = False) -> None:
    """
    NOT TESTED
    Convenience function to open the file explorer in the
    directory of the file and optionally highlighting it
    :param file_or_directory_path: Path to the file or directory to be opened
    :param highlight: Hightlight the directory or path after opening
    :return: None
    """
    file_or_directory_path = convert_file_path_to_string(
        file_or_directory_path
    )
    command_list = None
    if CURRENT_MACHINE == "Windows":
        command_list = [
            "explorer",
            f"{'/select,' if highlight else ''}{file_or_directory_path}"
        ]
    elif CURRENT_MACHINE == "Darwin":
        command_list = [
            "open",
            "-R" if highlight else '',
            f'"{file_or_directory_path}"'
        ]
    else:
        # Cross-platfrom highlighting is not yet implemented
        # in linux and other operating systems...
        command_list = [
            "xdg-open",
            f'"{file_or_directory_path}"'
        ]
    subprocess.Popen(command_list)
