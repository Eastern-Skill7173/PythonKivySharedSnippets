import json
import re
from datetime import datetime
from typing import (
    Callable,
    Optional,
    Iterable,
    Dict,
    Any,
)
from src.type_aliases import (
    Number,
    FilePath,
)
from src.constants.measurement_units import (
    HOUR,
    MINUTE,
)
from pathlib import Path
from threading import Thread

__all__ = (
    "threaded",
    "convert_file_path_to_string",
    "convert_string_to_file_path",
    "get_number_of_digits",
    "is_plural",
    "shuffle",
    "move_index",
    "replace_index",
    "validate_url",
    "matched_prefix",
    "matched_prefix_dict",
    "human_readable_size",
    "human_readable_duration",
    "human_readable_timestamp",
    "read_json_file",
    "write_to_json_file",
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


def convert_file_path_to_string(file_path: FilePath) -> str:
    """
    Convenience/Semantic function to convert a file path to a string
    :param file_path: String or object to convert
    :return: str
    """
    return str(file_path)


def convert_string_to_file_path(file_path: FilePath) -> Path:
    """
    Convenience/Semantic function to convert a file path to a path obj
    :param file_path: String or object to convert
    :return: str
    """
    return Path(file_path)


def get_number_of_digits(
        number: Number,
        count_post_decimal: bool = False) -> int:
    """
    Convenience function to get the number of digits in a number
    :param number: Number (int or float) to get the number of digits of
    :param count_post_decimal:
    Whether to include the numbers after the decimal point or not
    :return: int
    """
    clean_string = re.sub(
        f"[-{'.' if count_post_decimal else ''}]", '', str(number)
    )
    return len(clean_string)


def is_plural(number: int) -> bool:
    """
    Convenience function to check if a number is plural or not
    :param number: Given number to check if plural
    :return: bool
    """
    return number == 0 or number > 1


def matched_prefix(
        string: str,
        prefixes: Iterable[str],
        default_value=None) -> Optional[str]:
    """
    Convenience function to check which of the given prefixes,
    matches the string first.
    If none of them do, the `default_value` is returned
    :param string: String to be matched against
    :param prefixes: Iterable of prefixes to match to the string
    :param default_value:
    Default value to return if none of the prefixes match the string
    :return: Optional[str]
    """
    found_matched_prefix = default_value
    for prefix in prefixes:
        if string.startswith(prefix):
            found_matched_prefix = prefix
            break
    return found_matched_prefix


def matched_prefix_dict(
        string: str,
        prefix_dicts: Dict[str, Any],
        default_value=None) -> Optional[Any]:
    """
    Convenience function to check
    which of the given prefixes matches the string first,
    then return the value of the same key in the dictionary.
    If none of them do, the `default_value` is returned
    :param string: String to be matched against
    :param prefix_dicts: Dictionary of prefixes to match to the string
    :param default_value:
    Default value to return if none of the prefixes match the string
    :return: Optional[Any]
    """
    found_matched_prefix = default_value
    for prefix, value in prefix_dicts.items():
        if string.startswith(prefix):
            found_matched_prefix = value
            break
    return found_matched_prefix


def human_readable_duration(seconds: Number) -> str:
    """
    Convenience function to convert duration of an audio file
    (in seconds) to a human-readable form.
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


def human_readable_timestamp(
        timestamp: Number,
        string_format: str = "%Y-%m-%d | %H:%M:%S") -> str:
    """
    Convenience function to convert a timestamp
    to a human-readable format with the specified formatting
    :param timestamp: Timestamp value to be converted (e.g time.time())
    :param string_format:
    General format for the conversion return value to be based on
    :return: str
    """
    return datetime.fromtimestamp(timestamp).strftime(string_format)


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
