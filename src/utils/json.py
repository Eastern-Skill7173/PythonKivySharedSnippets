import json
from typing import Optional
from src.type_aliases import FilePath
from src.utils import convert_file_path_to_string

__all__ = (
    "read_json_file",
    "write_to_json_file",
    "JsonTree",
)


def read_json_file(file_path: FilePath, silent: bool = True) -> Optional[dict]:
    """
    Convenience function to read a json file with catching exceptions
    :param file_path: Path to the json file
    :param silent: Whether to ignore exceptions or not
    :return: Optional[dict]
    """
    file_path = convert_file_path_to_string(file_path)
    content = None
    exception = None
    try:
        with open(file_path, 'r') as json_file:
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


class JsonTree:
    """
    Class to take a file path referring to a json file
    and registering its content (key, value pair)
    """

    def __init__(self, json_path: FilePath):
        self._json_path = json_path
        self._json_content = read_json_file(self._json_path)
        parsed_tree = {
            key: value if not isinstance(value, dict) else type(self)(value)
            for key, value in self._json_content.items()
        }
        self.__dict__.update(parsed_tree)

    def apply_updates(
                self,
                indent: int = 4,
                sort_keys: bool = False,
                silent: bool = True) -> None:
        """
        Method to write the changed values to the json file-path given
        during initialization of the object
        :param indent: Indentation to be used when writing to the json file.
        Defaults to 4.
        :param sort_keys: Whether to alphabetically sort the keys
        when writing to th json file or not. Defaults to False.
        :param silent: Whether to handle exceptions silently. Defaults to True
        :return: None
        """
        changed_values = {
            key: self.__dict__[key] for key in self._json_content.keys()
        }
        self._json_content.update(changed_values)
        write_to_json_file(
            content=self._json_content,
            path=self._json_path,
            indent=indent,
            sort_keys=sort_keys,
            silent=silent,
        )

    @property
    def json_path(self) -> str:
        return self._json_path
