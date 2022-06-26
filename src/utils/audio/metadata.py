import stagger
from pathlib import Path
from typing import Optional, Final
from src.type_aliases import FilePath
from src.utils import convert_file_path_to_string

__all__ = (
    "AudioMetadata",
)


def _convert_lyrics_registration_value_to_tag(
        string_or_tag: Optional[str, stagger.id3.USLT]) -> stagger.id3.USLT:
    """
    Private function to check & convert a lyrics' registration value to an id3 USLT tag
    :param string_or_tag: Lyrics value to check and convert
    :return: stagger.id3.USLT
    """
    if isinstance(string_or_tag, str):
        id3_uslt_tag = stagger.id3.USLT(text=string_or_tag)
    elif isinstance(string_or_tag, stagger.id3.USLT):
        id3_uslt_tag = string_or_tag
    else:
        raise TypeError("lyrics value must be either a str or a stagger.id3.USLT")
    return id3_uslt_tag


class AudioMetadata:
    """
    Utility class to extract ID3v1/ID3v2 tags inside a local audio file
    """

    __slots__ = (
        "_source",
        "_core_metadata",
        "_tags_available",
        "_title",
        "_album",
        "_artist",
        "_genre",
        "_date",
        "_lyrics",
        "_cover",
    )
    _ALLOWED_PATH_TYPES: Final = (str, Path)
    """
    Private tuple containing allowed types for the source
    """

    def __init__(self, source: FilePath, silent: bool = False, **default_values) -> None:
        self._source = convert_file_path_to_string(source)
        self._core_metadata = None
        self._tags_available = False
        self._title = None
        self._album = None
        self._artist = None
        self._genre = None
        self._date = None
        self._lyrics = None
        self._cover = None
        self.update_fetched_tags(silent=silent, **default_values)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(" \
               f"source={self._source!r}, " \
               f"tags_available={self._tags_available!r}" \
               f")"

    def update_fetched_tags(self, silent: bool = False, **default_values) -> None:
        """
        Method to re-extract the tags of the already given source path (`self._source`)
        :param silent: Whether to pass exceptions silently
        :param default_values: A Pair of keyword arguments representing values to be used in case
        the given attr was not packed with the file or there was an error
        :return: None
        """
        self._core_metadata = None
        exception = None
        default_title = default_values.get("title")
        default_album = default_values.get("album")
        default_artist = default_values.get("artist")
        default_genre = default_values.get("genre")
        default_date = default_values.get("date")
        default_lyrics = default_values.get("lyrics")
        default_cover = default_values.get("cover")
        try:
            self._core_metadata = stagger.read_tag(self._source)
            self._tags_available = True
            self._title = self._core_metadata.title if self._core_metadata.title else default_title
            self._album = self._core_metadata.album if self._core_metadata.album else default_album
            self._artist = self._core_metadata.artist if self._core_metadata.artist else default_artist
            self._genre = self._core_metadata.genre if self._core_metadata.genre else default_genre
            self._date = self._core_metadata.date if self._core_metadata.date else default_date
            try:
                self._lyrics = self._core_metadata[stagger.id3.USLT][0].text
            except KeyError:
                self._lyrics = default_lyrics
            try:
                self._cover = self._core_metadata[stagger.id3.APIC][0].data
            except KeyError:
                self._cover = default_cover
        except FileNotFoundError as file_not_found_exception:
            exception = file_not_found_exception
        except stagger.errors.NoTagError as no_tag_error:
            self._tags_available = False
            exception = no_tag_error
        if exception:
            if silent:
                self._title = default_title
                self._album = default_album
                self._artist = default_artist
                self._genre = default_genre
                self._date = default_date
                self._lyrics = default_lyrics
                self._cover = default_cover
            else:
                raise exception

    def write(self, silent: bool = False, **new_tags) -> None:
        """
        Method to write new values for the tags of the audio file
        :param silent: Whether to pass exceptions silently or not
        :param new_tags: List of keyword arguments holding new values for each tag
        :return: None
        """
        exception = None
        new_title = new_tags.get("title")
        new_album = new_tags.get("album")
        new_artist = new_tags.get("artist")
        new_genre = new_tags.get("genre")
        new_date = new_tags.get("date")
        new_lyrics = new_tags.get("lyrics")
        new_cover = new_tags.get("cover")
        try:
            if new_title:
                self._title = self._core_metadata.title = new_title
            if new_album:
                self._album = self._core_metadata.album = new_album
            if new_artist:
                self._artist = self._core_metadata.artist = new_artist
            if new_genre:
                self._genre = self._core_metadata.genre = new_genre
            if new_date:
                self._date = self._core_metadata.date = new_date
            if new_lyrics:
                converted_lyrics_id3_tag = _convert_lyrics_registration_value_to_tag(new_lyrics)
                self._lyrics = self._core_metadata[stagger.id3.USLT] = converted_lyrics_id3_tag
            if new_cover:
                self._cover = self._core_metadata.picture = new_cover
            self._core_metadata.write()
        except ValueError as value_error:
            exception = value_error
        if exception and not silent:
            raise exception

    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, new_source: FilePath) -> None:
        if not isinstance(new_source, self._ALLOWED_PATH_TYPES):
            raise TypeError(f"paths can only be from {self._ALLOWED_PATH_TYPES!r}")
        self._source = convert_file_path_to_string(new_source)
        self.update_fetched_tags()

    @property
    def core_metadata(self):
        # You still have access to the internally used metadata
        # In case you wanted to view the raw data without changes applied to it
        return self._core_metadata

    @property
    def tags_available(self) -> bool:
        return self._tags_available

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
