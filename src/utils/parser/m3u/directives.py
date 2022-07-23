import os
import re
from src.type_aliases import Number, FilePath
from typing import Final, Optional

__all__ = (
    "EXTM3U",
    "EXTINF",
    "PLAYLIST",
    "EXTGRP",
    "EXTALB",
    "EXTART",
    "EXTGENRE",
    "EXTM3A",
    "EXTBYT",
    "EXTBIN",
    "EXTENC",
    "EXTIMG",
    "ALL_DIRECTIVE_PREFIXES",
)


class _Directive:
    """
    Base class defining the skeleton of a directive in M3U.
    Class CANNOT be used on its own
    """
    LEADING_CHARACTER: Final = '#'
    """
    Leading character for every directive definition in M3U
    """
    SEPARATOR_CHARACTER: Final = ':'
    """
    Separator character for directives that allow parameters
    """
    supports_parameters = False
    """
    Whether the directive allows passing parameters or not
    """

    def __init__(self):
        separator_character = ''
        if self.supports_parameters:
            separator_character = self.SEPARATOR_CHARACTER
        self._as_m3u = f"{self.LEADING_CHARACTER}" \
                       f"{type(self).__name__}" \
                       f"{separator_character}"
        self._m3u_string_parameters = ''

    def __repr__(self) -> str:
        return f"{type(self).__name__}(as_m3u={self._as_m3u!r})"

    @classmethod
    def from_m3u_string(cls, m3u_string: str):
        return cls()

    @classmethod
    def _separate_parameters_from_directive(
            cls,
            m3u_string: str) -> Optional[str]:
        """
        Private class-method to separate parameters from extended directives
        :param m3u_string: The string to separate parameters from
        :return: str
        """
        if cls.supports_parameters:
            return m3u_string.split(cls.SEPARATOR_CHARACTER)[-1]

    @property
    def as_m3u(self) -> str:
        return self._as_m3u


class EXTM3U(_Directive):  # NOQA
    """
    File header directive, must be the first line of the file
    """


class EXTINF(_Directive):  # NOQA
    """
    Directive supplying parameters including track information:
    runtime in seconds and title of the following resource.
    Additional properties could also be included as key-value pairs
    """
    supports_parameters = True
    TIME_SEPARATOR: Final = ','
    """
    Separator used for differentiating track length from other properties
    """
    ARTIST_TITLE_SEPARATOR: Final = '-'
    """
    Separator used for differentiating track artist and title
    from other properties
    """
    _compiled_separator = re.compile(
        f"[{TIME_SEPARATOR}{ARTIST_TITLE_SEPARATOR}]",
        flags=re.IGNORECASE
    )
    """
    Compiled regex pattern separating each of track length, artist,
    and title from string
    """

    def __init__(self, track_length: Number, artist: str, title: str):
        super(EXTINF, self).__init__()
        self._track_length = int(track_length)
        self._artist = str(artist).strip()
        self._title = str(title).strip()
        self._as_m3u += f"{self._track_length}" \
                        f"{self.TIME_SEPARATOR} " \
                        f"{self._artist} " \
                        f"{self.ARTIST_TITLE_SEPARATOR} " \
                        f"{self._title}"

    @classmethod
    def from_m3u_string(cls, m3u_string: str):
        parsed_external_info = cls._compiled_separator.split(
            cls._separate_parameters_from_directive(m3u_string)
        )
        track_length, artist, title = parsed_external_info
        track_length = int(track_length.strip())
        return cls(track_length=track_length, artist=artist, title=title)

    @property
    def track_length(self) -> float:
        return self._track_length

    @property
    def artist(self) -> str:
        return self._artist

    @property
    def title(self) -> str:
        return self._title


class PLAYLIST(_Directive):
    """
    Directive supplying single parameter indicating playlist display title
    """
    supports_parameters = True

    def __init__(self, playlist_title: str):
        super(PLAYLIST, self).__init__()
        self._playlist_title = str(playlist_title).strip()
        self._as_m3u += self._playlist_title

    @classmethod
    def from_m3u_string(cls, m3u_string: str):
        playlist_title = cls._separate_parameters_from_directive(m3u_string)
        return cls(playlist_title=playlist_title)

    @property
    def playlist_title(self) -> str:
        return self._playlist_title


class EXTGRP(_Directive):  # NOQA
    """
    Directive supplying parameters for named grouping
    """
    supports_parameters = True

    def __init__(self, group: str):
        super(EXTGRP, self).__init__()
        self._group = str(group).strip()
        self._as_m3u += self._group

    @classmethod
    def from_m3u_string(cls, m3u_string: str):
        group = cls._separate_parameters_from_directive(m3u_string)
        return cls(group=group)

    @property
    def group(self) -> str:
        return self._group


class EXTALB(_Directive):  # NOQA
    """
    Directive supplying single parameter indicating album information,
    title in particular
    """
    supports_parameters = True

    def __init__(self, album_info: str):
        super(EXTALB, self).__init__()
        self._album_info = str(album_info).strip()
        self._as_m3u += self._album_info

    @classmethod
    def from_m3u_string(cls, m3u_string: str):
        album_info = cls._separate_parameters_from_directive(m3u_string)
        return cls(album_info=album_info)

    @property
    def album_info(self) -> str:
        return self._album_info


class EXTART(_Directive):  # NOQA
    """
    Directive supplying single parameter indicating album artist
    """
    supports_parameters = True

    def __init__(self, artist: str):
        super(EXTART, self).__init__()
        self._artist = str(artist).strip()
        self._as_m3u += self._artist

    @classmethod
    def from_m3u_string(cls, m3u_string: str):
        artist = cls._separate_parameters_from_directive(m3u_string)
        return cls(artist=artist)

    @property
    def artist(self) -> str:
        return self._artist


class EXTGENRE(_Directive):  # NOQA
    """
    Directive supplying single parameter indicating album genre
    """
    supports_parameters = True

    def __init__(self, genre: str):
        super(EXTGENRE, self).__init__()
        self._genre = str(genre).strip()
        self._as_m3u += self._genre

    @classmethod
    def from_m3u_string(cls, m3u_string: str):
        genre = cls._separate_parameters_from_directive(m3u_string)
        return cls(genre=genre)

    @property
    def genre(self) -> str:
        return self._genre


class EXTM3A(_Directive):  # NOQA
    """
    Directive for playlists or chapters of an album in a single file
    """


class EXTBYT(_Directive):  # NOQA
    """
    Directive supplying single parameter indicating file size in bytes
    """
    supports_parameters = True

    def __init__(self, size_in_bytes: Number):
        super(EXTBYT, self).__init__()
        self._size_in_bytes = int(size_in_bytes)
        self._as_m3u += f"{self._size_in_bytes}"

    @classmethod
    def from_m3u_string(cls, m3u_string: str):
        size_in_bytes = int(
            cls._separate_parameters_from_directive(m3u_string).strip()
        )
        return cls(size_in_bytes=size_in_bytes)

    @property
    def size_in_bytes(self) -> int:
        return self._size_in_bytes


class EXTBIN(_Directive):  # NOQA
    """
    Directive supplying single binary parameter, usually concatenated MP3s
    """
    supports_parameters = True


class EXTENC(_Directive):  # NOQA
    """
    Directive supplying single parameter indicating text encoding.
    Must be the second line of the file
    """
    supports_parameters = True

    def __init__(self, encoding: str):
        super(EXTENC, self).__init__()
        self._encoding = str(encoding).strip()
        self._as_m3u += self._encoding

    @classmethod
    def from_m3u_string(cls, m3u_string: str):
        encoding = cls._separate_parameters_from_directive(m3u_string)
        return cls(encoding=encoding)

    @property
    def encoding(self) -> str:
        return self._encoding


class EXTIMG(_Directive):  # NOQA
    """
    Directive supplying single parameter for cover, logo or other image
    """
    supports_parameters = True
    supported_image_file_extensions = (".jpg", ".png",)
    """
    Tuple of strings indicating supported image file extensions
    to be filtered out
    """

    def __init__(
            self,
            cover_img: FilePath,
            validate_existence: bool = True,
            check_extension: bool = True):
        super(EXTIMG, self).__init__()
        self._cover_img = str(cover_img).strip()
        self._as_m3u += self._cover_img
        self._exists = None
        self._is_supported = None
        if validate_existence:
            self._exists = os.path.exists(self._cover_img)
        if check_extension:
            self._is_supported = \
                self._cover_img.endswith(self.supported_image_file_extensions)

    @classmethod
    def from_m3u_string(cls, m3u_string: str):
        cover_img = cls._separate_parameters_from_directive(m3u_string)
        return cls(cover_img=cover_img)

    @property
    def cover_img(self) -> str:
        return self._cover_img

    @property
    def exists(self) -> bool:
        return self._exists

    @property
    def is_supported(self) -> bool:
        return self._is_supported


ALL_DIRECTIVE_PREFIXES: Final = {
    f"{_Directive.LEADING_CHARACTER}{cls.__name__}": cls
    for cls in _Directive.__subclasses__()
}
