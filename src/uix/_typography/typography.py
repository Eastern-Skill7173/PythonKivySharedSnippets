from src.type_aliases import FilePath
from src.utils import (
    convert_file_path_to_string,
    read_json_file,
    write_to_json_file,
)


__all__ = (
    "TypoGraphy",
)


class TypoGraphy:
    """
    Utility class to load a json file with as a typography reference
    """

    def __init__(self, json_typography_path: FilePath):
        self._json_typography_path = convert_file_path_to_string(
            json_typography_path
        )
        self._typography_dict = read_json_file(self._json_typography_path)
        self.__dict__.update(self._typography_dict)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(" \
            f"json_typography_path={self._json_typography_path!r})"

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
            key: self.__dict__[key] for key in self._typography_dict.keys()
        }
        self._typography_dict.update(changed_values)
        write_to_json_file(
            content=self._typography_dict,
            path=self._json_typography_path,
            indent=indent,
            sort_keys=sort_keys,
            silent=silent,
        )

    @property
    def json_typography_path(self) -> str:
        return self._json_typography_path
