import os
import subprocess
import json
import webbrowser
import constants
from typing import Callable, Union, Optional
from threading import Thread
from kivy import platform
from kivy.logger import LoggerHistory

__all__ = (
    "threaded",
    "human_readable_size",
    "human_readable_duration",
    "get_logger_history",
    "read_json_file",
    "write_to_json_file",
    "switch_screen",
    "open_link",
    "open_file",
)


def threaded(function: Callable):
    """Decorator to run function/method in a thread."""

    def _run_in_thread(*args, **kwargs) -> Thread:
        thread = Thread(target=function,
                        daemon=True,
                        args=args,
                        kwargs=kwargs
                        )
        thread.start()
        return thread

    return _run_in_thread


def human_readable_size(size_in_bytes: Union[int, float], rounding_point: int = 2) -> str:
    """
    Convenience function to convert size in bytes to a human-readable form
    :param size_in_bytes: Size of a file or object in bytes
    :param rounding_point: Position of the floating point for the `round` built-in
    :return: str
    """
    if size_in_bytes >= constants.GIGABYTE:
        string_converted_size = f"{round(size_in_bytes / constants.GIGABYTE, rounding_point)} GB"
    elif size_in_bytes >= constants.MEGABYTE:
        string_converted_size = f"{round(size_in_bytes / constants.MEGABYTE, rounding_point)} MB"
    elif size_in_bytes >= constants.KILOBYTE:
        string_converted_size = f"{round(size_in_bytes / constants.KILOBYTE, rounding_point)} KB"
    else:
        string_converted_size = f"{size_in_bytes} Bytes"
    return string_converted_size


def human_readable_duration(seconds: Union[int, float]) -> str:
    """
    Convenience function to convert duration of an audio file in seconds to a human-readable form.
    :param seconds: Length of an audio file in seconds
    :return: str
    """
    if seconds >= constants.HOUR:
        string_converted_duration = \
            f"{int(seconds // constants.HOUR)}:" \
            f"{int(seconds % constants.HOUR // constants.MINUTE):02d}:" \
            f"{int(seconds % constants.HOUR % constants.MINUTE):02d}"
    elif seconds >= constants.MINUTE:
        string_converted_duration = \
            f"{int(seconds // constants.MINUTE)}:" \
            f"{int(seconds % constants.MINUTE):02d}"
    else:
        string_converted_duration = f"0:{int(seconds):02d}"
    return string_converted_duration


def get_logger_history() -> str:
    """
    Convenience function to get logger history
    :return: str
    """
    return '\n'.join(log_record.message for log_record in reversed(LoggerHistory.history))


def read_json_file(path: str) -> Optional[dict]:
    """
    Convenience function to read a json file with catching exceptions
    :param path: Path to the json file
    :return: Optional[dict]
    """
    content = None
    try:
        with open(path, 'r') as json_file:
            content = json.load(json_file)
    except FileNotFoundError:
        pass
    except json.decoder.JSONDecodeError:
        pass
    return content


def write_to_json_file(content,
                       path: str,
                       indent: int = 4,
                       sort_keys: bool = False,
                       silent: bool = True) -> None:
    """
    Convenience function to write the given content to a json file
    :param content: Content to write to the json file
    :param path: Path to the json file
    :param indent: Indentation to be used for writing to the json file
    :param sort_keys: Whether to sort keys when writing or not
    :param silent: Whether to silently pass exceptions or not
    :return: None
    """
    try:
        with open(path, 'w') as json_file:
            json.dump(content, json_file, indent=indent, sort_keys=sort_keys)
    except TypeError as type_error:
        if not silent:
            raise type_error


def switch_screen(screen_manager,
                  screen: str,
                  direction: Optional[str] = None,
                  beginning_transition: Optional = None,
                  ending_transition: Optional = None) -> None:
    """
    Convenience method for switching screens between screen managers
    :param screen_manager: The targeted `ScreenManager` instance
    :param screen: The desired screen to switch to
    :param direction: The direction of `screen_manager` transition
    :param beginning_transition: The transition to use before switching screens
    :param ending_transition: The transition to use after switching screens
    :return: None
    """
    if beginning_transition:
        screen_manager.transition = beginning_transition
    if direction:
        screen_manager.transition.direction = direction
    screen_manager.current = screen
    if ending_transition:
        screen_manager.transition = ending_transition


def open_link(link: str) -> None:
    """
    Convenience function to open the given url in user's default browser
    :param link: URL Address to be opened in user's default browser
    :return: None
    """
    webbrowser.open(link, new=2, autoraise=True)


def open_file(file_path: str) -> None:
    """
    Convenience function to open the given file path with the default program
    across all `Linux`, `OSX`, `Windows`
    :param file_path: Path to the file to be opened
    :return: None
    """
    if platform == "win":
        os.startfile(file_path)
    elif platform == "macosx":
        subprocess.Popen(["open", file_path])
    else:
        subprocess.Popen(["xdg-open", file_path])
