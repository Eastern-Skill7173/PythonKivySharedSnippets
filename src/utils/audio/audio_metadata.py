import stagger
from pathlib import Path
from typing import Union, Optional, Final

__all__ = (
    "AudioMetadata",
)


class AudioMetadata:
    """
    Utility class to extract ID3v1/ID3v2 tags inside a local audio file
    """
    __slots__ = (
        "_source",
        "_core_metadata",
        "_title",
        "_album",
        "_artist",
        "_genre",
        "_lyrics",
        "_cover",
    )
    _ALLOWED_PATH_TYPES: Final = (str, Path)
    """
    Private tuple containing allowed types for the source
    """
    default_title: Optional[str] = None
    """
    Default value for the title attr if not provided by the file
    """
    default_album: Optional[str] = None
    """
    Default value for the album attr if not provided by the file
    """
    default_artist: Optional[str] = None
    """
    Default value for the artist attr if not provided by the file
    """
    default_genre: Optional[str] = None
    """
    Default value for the genre attr if not provided by the file
    """
    default_lyrics: Optional[str] = None
    """
    Default value for the lyrics attr if not provided by the file
    """
    default_cover: Optional = None
    """
    Default value for the cover attr if not provided by the file
    """

    def __init__(self, source: Union[str, Path]) -> None:
        self._source = str(source)
        self._core_metadata = stagger.read_tag(self._source)
        self._title = self._core_metadata.title if self._core_metadata.title else self.default_title
        self._album = self._core_metadata.album if self._core_metadata.album else self.default_album
        self._artist = self._core_metadata.artist if self._core_metadata.artist else self.default_artist
        self._genre = self._core_metadata.genre if self._core_metadata.genre else self.default_genre
        try:
            self._lyrics = self._core_metadata[stagger.id3.USLT][0].text
        except KeyError:
            self._lyrics = self.default_lyrics
        try:
            self._cover = self._core_metadata[stagger.id3.APIC][0].data
        except KeyError:
            self._cover = self.default_cover

    def __repr__(self) -> str:
        return f"{type(self).__name__}(source={self._source!r})"

    def apply_defaults(self) -> None:
        """
        Method to apply the class-level default values to the instance variables
        :return: None
        """
        self._title = self.default_title
        self._album = self.default_album
        self._artist = self.default_artist
        self._genre = self.default_genre
        self._lyrics = self.default_lyrics
        self._cover = self.default_cover

    def update_fetched_tags(self) -> None:
        """
        Method to re-extract the tags of the already given source path (`self._source`)
        :return: None
        """
        self._core_metadata = stagger.read_tag(self._source)
        self._title = self._core_metadata.title if self._core_metadata.title else self.default_title
        self._album = self._core_metadata.album if self._core_metadata.album else self.default_album
        self._artist = self._core_metadata.artist if self._core_metadata.artist else self.default_artist
        self._genre = self._core_metadata.genre if self._core_metadata.genre else self.default_genre
        try:
            self._lyrics = self._core_metadata[stagger.id3.USLT][0].text
        except KeyError:
            self._lyrics = self.default_lyrics
        try:
            self._cover = self._core_metadata[stagger.id3.APIC][0].data
        except KeyError:
            self._cover = self.default_cover

    @property
    def source(self) -> str:
        return self._source

    @source.setter
    def source(self, new_source: Union[str, Path]) -> None:
        if not isinstance(new_source, self._ALLOWED_PATH_TYPES):
            raise TypeError(f"paths can only be from {self._ALLOWED_PATH_TYPES!r}")
        self._source = str(new_source)
        self.update_fetched_tags()

    @property
    def core_metadata(self):
        # You still have access to the internally used metadata
        # In case you wanted to view the raw data without changes applied to it
        return self._core_metadata

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
    def lyrics(self):
        return self._lyrics

    @property
    def cover(self):
        return self._cover
