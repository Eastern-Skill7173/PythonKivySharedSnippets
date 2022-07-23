"""
Module is still NOT implemented
"""


import os.path
from typing import TextIO, Optional
from src.type_aliases import FilePath
from src.utils import matched_prefix_dict
from src.utils.parser.m3u.directives import ALL_DIRECTIVE_PREFIXES, EXTINF

__all__ = (
    "AudioFileRef",
    "AudioDirRef",
    "M3UParser",
)


class AudioFileRef:
    """
    Class representing an audio file in an M3U file
    """
    supported_audio_file_extensions = (".mp3",)
    """
    Tuple of strings indicating supported audio file extensions
    (during additions unsupported formats will be filtered out)
    """

    def __init__(self,
                 source: FilePath,
                 external_info: Optional[EXTINF] = None,
                 validate_existence: bool = True,
                 check_extension: bool = True):
        self._source = str(source)
        self._external_info = external_info
        self._exists = None
        self._is_supported = None
        if validate_existence:
            self._exists = os.path.exists(self._source)
        if check_extension:
            self._is_supported = self._source.endswith(
                self.supported_audio_file_extensions
            )

    def __repr__(self) -> str:
        return f"{type(self).__name__}(source={self._source!r})"

    @property
    def source(self) -> str:
        return self._source

    @property
    def external_info(self):
        return self._external_info

    @property
    def exists(self) -> bool:
        return self._exists

    @property
    def is_supported(self) -> bool:
        return self._is_supported


class AudioDirRef:
    """
    Class representing a directory of audio files in an M3U file
    """

    def __init__(self,
                 directory: FilePath,
                 validate_existence: bool = True,
                 validate_directory: bool = True,
                 check_extension: bool = True):
        self._directory = str(directory)
        self._audio_files = tuple(
            AudioFileRef(file, check_extension=check_extension)
            if check_extension
            else file for file in os.listdir(self._directory)
        )
        self._exists = None
        self._is_dir = None
        if validate_existence:
            self._exists = os.path.exists(self._directory)
        if validate_directory:
            self._is_dir = os.path.isdir(self._directory)

    def __repr__(self) -> str:
        return f"{type(self).__name__}(directory={self._directory!r})"

    def __iter__(self):
        for audio_file in self._audio_files:
            yield audio_file

    @property
    def directory(self) -> str:
        return self._directory

    @property
    def exists(self) -> bool:
        return self._exists

    @property
    def is_dir(self) -> bool:
        return self._is_dir


class M3UParser:
    """
    Class allowing for parsing of `M3U` to `python` and `python` to `M3U`
    """

    @classmethod
    def dump(cls, file_type: TextIO) -> None:
        """
        Class-method to dump python content into M3U strings
        :return: None
        """
        file_type.write(
            cls.dumps()
        )

    @classmethod
    def load(cls, file_type: TextIO) -> list:
        """
        Class-method to load a text file type M3U file into python
        :param file_type: The opened text file
        :return:
        """
        return cls.loads(
            file_type.read()
        )

    @classmethod
    def dumps(cls, *args) -> str:
        """
        Class-method to dump python content into M3U strings
        :return: str
        """
        # '\n'.join(m3u_obj.as_m3u for m3u_obj in args)
        m3u_string = ''
        for m3u_obj in args:
            if isinstance(m3u_obj, AudioFileRef):
                external_info_string = ''
                if m3u_obj.external_info:
                    external_info_string = m3u_obj.external_info.as_m3u
                m3u_string += f"{external_info_string}\n{m3u_obj.source}"
            elif isinstance(m3u_obj, AudioDirRef):
                m3u_string += m3u_obj.directory
            else:
                m3u_string += m3u_obj.as_m3u
            m3u_string += '\n'
        return m3u_string

    @classmethod
    def loads(cls, string: str) -> list:
        """
        Class-method to load a multi-lined M3U string into python
        :param string: The string to parse
        :return: list
        """
        file_structure = []
        last_external_info = None
        for line in string.splitlines():
            found_matched_prefix = matched_prefix_dict(
                line, ALL_DIRECTIVE_PREFIXES
            )
            if found_matched_prefix:
                directive_obj = found_matched_prefix.from_m3u_string(line)
                file_structure.append(directive_obj)
                if isinstance(directive_obj, EXTINF):
                    last_external_info = directive_obj
            else:
                if not line.isspace():
                    file_structure.append(
                        AudioFileRef(line, external_info=last_external_info)
                    )
                    last_external_info = None
        return file_structure
