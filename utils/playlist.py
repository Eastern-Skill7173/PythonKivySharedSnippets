from typing import Optional
from utils import shuffle, is_plural
from kivy.core.audio import Sound

__all__ = (
    "Playlist",
)


# TODO: add support for loading and saving as m3u files
class Playlist:
    """
    Utility class for playlist like behavior
    """
    __slots__ = (
        "_name",
        "_songs",
    )
    _used_names = []
    """
    List of used names
    """
    allowed_classes = [Sound, str]
    """
    List of class names to check against
    """

    def __init__(self, name: str, *args):
        self._update_used_names(name)
        self._name = name
        self._songs = []
        self.add(*args)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self._name!r}, length={self.__len__()})"

    def __contains__(self, item) -> bool:
        return item in self._songs

    def __len__(self) -> int:
        return len(self._songs)

    def __iter__(self):
        for song in self._songs:
            yield song

    def __getitem__(self, item):
        return self._songs.__getitem__(item)

    def __del__(self):
        """
        Remove the playlist's used name when deleted
        """
        self._used_names.remove(self._name)

    @classmethod
    def used_names(cls):
        """
        Class-method to yield the used playlist names
        """
        for used_name in cls._used_names:
            yield used_name

    @classmethod
    def _check_playlist_name(cls, name: str) -> None:
        """
        Class-method to validate the given name against certain checks
        :param name: The name to be checked
        :return: None
        """
        if not isinstance(name, str):
            raise TypeError("name must be a string")
        if not name:
            raise ValueError("name cannot be empty")
        if name in cls._used_names:
            raise ValueError(f"name {name!r} already has been used for another playlist")

    @classmethod
    def _check_object_class(cls, *args) -> None:
        """
        Class-method to check that arguments are of the allowed types
        :param args: List of initialized objects to check against allowed classes
        :return: None
        """
        for obj in args:
            # `is_instance` only accepts tuples
            if not isinstance(obj, tuple(cls.allowed_classes)):
                raise TypeError(f"only {cls.allowed_classes} are allowed")

    @classmethod
    def _update_used_names(cls, name: str) -> None:
        """
        Class-method to check the given name, upon passing add the name to the used names
        :param name: The given name to be checked, then added to the used names
        :return: None
        """
        cls._check_playlist_name(name)
        cls._used_names.append(name)

    def shuffle(self, return_copy: bool = True) -> Optional[list]:
        """
        Method to shuffle the playlist's songs, whether in-place or as a copied list
        :param return_copy: Return the shuffled songs as a copied list or shuffle in-place
        :return: Optional[list]
        """
        return shuffle(self._songs, return_copy=return_copy)

    def add(self, *args) -> None:
        """
        Method to add strings or sound objects to playlist
        :param args: List of string or sound objects to be added to playlist
        :return: None
        """
        self._check_object_class(*args)
        self._songs.extend(args)

    def pop(self, *args: int) -> None:
        """
        Method to pop indexes at given integers from the playlist
        :param args: List of indexes to be popped from playlist
        :return: None
        """
        for index in args:
            self._songs.pop(index)

    def remove(self, *args) -> None:
        """
        Method to remove the given values from the playlist
        :param args: List of values to be removed from the playlist
        :return: None
        """
        for song in args:
            self._songs.remove(song)

    def clear(self) -> None:
        """
        Method to clear the playlist
        :return: None
        """
        self._songs.clear()

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, new_name: str) -> None:
        self._update_used_names(new_name)
        self._name = new_name

    @property
    def string_length(self) -> str:
        current_length = self.__len__()
        return f"{current_length} song{'s' if is_plural(current_length) else ''}"
