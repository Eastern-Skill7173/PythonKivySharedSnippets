import os
from src.utils import human_readable_timestamp, human_readable_size
from src.utils.audio.metadata import AudioMetadata

__all__ = (
    "BaseSong",
)


class BaseSong:
    """
    Base class for any object representing a music/audio file.
    Used in `./youtube_music.py`, `./deezer.py`,
    `./spotify.py` & `./soundcloud.py`
    """

    __slots__ = (
        "_path",
        "_st_mtime",
        "_st_size",
        "_file_date",
        "_file_size",
        "_metadata",
        "_tags_available",
        "_title",
        "_album",
        "_artist",
        "_genre",
        "_date",
        "_lyrics",
        "_cover",
    )

    def __init__(self) -> None:
        self._path = None
        self._tags_available = False
        self._st_mtime = None
        self._st_size = None
        self._file_date = None
        self._file_size = None
        self._metadata = None
        self._title = None
        self._album = None
        self._artist = None
        self._genre = None
        self._date = None
        self._lyrics = None
        self._cover = None

    def fetch_info(self, silent: bool = True, **default_values):
        """
        Method to fetch information related to the audio file.
        (Method can also be called from the user in order
        to re-fetch the information)
        :param silent: Whether to pass exceptions silently or not
        :param default_values: A pair of keyword arguments representing default values
        to be used on exception or when no value is found
        :return: None
        """
        exception = None
        try:
            file_info = os.stat(self._path)
            self._metadata = AudioMetadata(self._path, silent=silent)
            self._tags_available = self._metadata.tags_available
            self._st_mtime = file_info.st_mtime
            self._st_size = file_info.st_size
            self._file_date = human_readable_timestamp(self._st_mtime)
            self._file_size = human_readable_size(self._st_size)
            self._title = self._metadata.title
            self._album = self._metadata.album
            self._artist = self._metadata.artist
            self._genre = self._metadata.genre
            self._date = self._metadata.date
            self._lyrics = self._metadata.lyrics
            self._cover = self._metadata.cover
        except FileNotFoundError as file_not_found_error:
            exception = file_not_found_error
        if exception and not silent:
            raise exception

    @property
    def path(self) -> str:
        return self._path

    @property
    def metadata(self):
        return self._metadata

    @property
    def tags_available(self):
        return self._tags_available

    @property
    def st_mtime(self):
        return self._st_mtime

    @property
    def st_size(self):
        return self._st_size

    @property
    def file_date(self):
        return self._file_date

    @property
    def file_size(self):
        return self._file_size

    @property
    def title(self):
        return self._title

    @property
    def album(self):
        return self._album

    @property
    def artist(self):
        return self._artist

    @property
    def genre(self):
        return self._genre

    @property
    def date(self):
        return self._date

    @property
    def lyrics(self):
        return self._lyrics

    @property
    def cover(self):
        return self._cover
