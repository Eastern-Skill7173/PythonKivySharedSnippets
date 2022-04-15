import os
import subprocess
import json
import webbrowser
import random
from typing import Callable, Union, Optional
from src.constants.measurement_units import (
    SIUnitsPrefixes,
    HOUR,
    MINUTE,
)
from pathlib import Path
from threading import Thread
from kivy import platform
from kivy.animation import Animation
from kivy.logger import LoggerHistory

__all__ = (
    "threaded",
    "is_plural",
    "shuffle",
    "move_index",
    "replace_index",
    "human_readable_size",
    "human_readable_duration",
    "update_animation_duration",
    "update_animation_transition",
    "update_animation_properties",
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


def is_plural(number: int) -> bool:
    """
    Convenience function to check if a number is plural or not
    :param number: Given number to check if plural
    :return: bool
    """
    return number == 0 or number > 1


def shuffle(list_obj: list, return_copy: bool = True) -> Optional[list]:
    """
    Convenience function to shuffle a list, whether in-place or as a copied list
    :param list_obj: The list instance to operate on
    :param return_copy: Return copy or shuffle in-place
    :return: Optional[list]
    """
    if return_copy:
        list_copy = list_obj.copy()
        random.shuffle(list_copy)
        return list_copy
    else:
        random.shuffle(list_obj)


def move_index(list_obj: list, element_index: int, target_index: int) -> None:
    """
    Convenience function to move an element within a list
    :param list_obj: The list instance to operate on
    :param element_index: The index of the current element to be moved
    :param target_index: The target index to move to
    :return: None
    """
    list_obj.insert(target_index, list_obj.pop(element_index))


def replace_index(list_obj: list, element_index: int, replacement_value) -> None:
    """
    Convenience function to replace an index's element with another value
    :param list_obj: The list instance to operate on
    :param element_index: The index of the element to be replaced
    :param replacement_value: Value to be put in place of the given index
    :return: None
    """
    list_obj.pop(element_index)
    list_obj.insert(element_index, replacement_value)


def human_readable_size(size_in_bytes: Union[int, float], rounding_point: int = 2) -> str:
    """
    Convenience function to convert size in bytes to a human-readable form
    :param size_in_bytes: Size of a file or object in bytes
    :param rounding_point: Position of the floating point for the `round` built-in
    :return: str
    """
    if size_in_bytes >= SIUnitsPrefixes.GIGA:
        string_converted_size = f"{round(size_in_bytes / SIUnitsPrefixes.GIGA, rounding_point)} GB"
    elif size_in_bytes >= SIUnitsPrefixes.MEGA:
        string_converted_size = f"{round(size_in_bytes / SIUnitsPrefixes.MEGA, rounding_point)} MB"
    elif size_in_bytes >= SIUnitsPrefixes.KILO:
        string_converted_size = f"{round(size_in_bytes / SIUnitsPrefixes.KILO, rounding_point)} KB"
    else:
        string_converted_size = f"{size_in_bytes} Bytes"
    return string_converted_size


def human_readable_duration(seconds: Union[int, float]) -> str:
    """
    Convenience function to convert duration of an audio file in seconds to a human-readable form.
    :param seconds: Length of an audio file in seconds
    :return: str
    """
    if seconds >= HOUR:
        string_converted_duration = \
            f"{int(seconds // HOUR)}:" \
            f"{int(seconds % HOUR // MINUTE):02d}:" \
            f"{int(seconds % HOUR % MINUTE):02d}"
    elif seconds >= MINUTE:
        string_converted_duration = \
            f"{int(seconds // MINUTE)}:" \
            f"{int(seconds % MINUTE):02d}"
    else:
        string_converted_duration = f"0:{int(seconds):02d}"
    return string_converted_duration


def update_animation_duration(animation_obj: Animation, new_duration: Union[int, float]) -> None:
    """
    Convenience function to update an `Animation` object's duration
    :param animation_obj: The `Animation` object to be updated
    :param new_duration: New duration to be set for the animation
    :return: None
    """
    super(animation_obj.__class__, animation_obj).__init__(
        duration=new_duration,
        transition=animation_obj.transition,
        **animation_obj.animated_properties
    )


def update_animation_transition(animation_obj: Animation, new_transition: str) -> None:
    """
    Convenience function to update an `Animation` object's transition
    :param animation_obj: The `Animation` object to be updated
    :param new_transition: New transition to be set for the animation
    :return: None
    """
    super(animation_obj.__class__, animation_obj).__init__(
        duration=animation_obj.duration,
        transition=new_transition,
        **animation_obj.animated_properties
    )


def update_animation_properties(
        animation_obj: Animation,
        clear_previous_items: bool = False,
        **kwargs) -> None:
    """
    Convenience function to update an `Animation` object's animated properties
    :param animation_obj: The `Animation` object to be updated
    :param clear_previous_items: Whether to clear the existing properties before updating
    :param kwargs: List of keyword arguments to update the animated properties
    :return: None
    """
    if clear_previous_items:
        animation_obj.animated_properties.clear()
    animation_obj.animated_properties.update(kwargs)


def get_logger_history() -> str:
    """
    Convenience function to get logger history
    :return: str
    """
    return '\n'.join(log_record.message for log_record in reversed(LoggerHistory.history))


def read_json_file(path: str, silent: bool = True) -> Optional[dict]:
    """
    Convenience function to read a json file with catching exceptions
    :param path: Path to the json file
    :param silent: Whether to ignore exceptions or not
    :return: Optional[dict]
    """
    content = None
    exception = None
    try:
        with open(path, 'r') as json_file:
            content = json.load(json_file)
    except FileNotFoundError as file_not_found_error:
        exception = file_not_found_error
    except json.decoder.JSONDecodeError as json_decode_error:
        exception = json_decode_error
    if not silent and exception:
        raise exception
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


def open_link(link: str, new: int = 2, auto_raise: bool = True) -> None:
    """
    Convenience function to open the given url in user's default browser
    :param link: URL Address to be opened in user's default browser
    :param new: Where to open the link ( in a new tab, existing tab or new page )
    :param auto_raise: Whether to raise the browser window or not
    :return: None
    """
    webbrowser.open(link, new=new, autoraise=auto_raise)


def open_file(file_path: Union[str, Path]) -> None:
    """
    Convenience function to open the given file path with the default program
    across all `Linux`, `OSX`, `Windows`
    :param file_path: Path to the file to be opened
    :return: None
    """
    file_path = str(file_path)
    if platform == "win":
        os.startfile(file_path)
    elif platform == "macosx":
        subprocess.Popen(["open", file_path])
    else:
        subprocess.Popen(["xdg-open", file_path])
