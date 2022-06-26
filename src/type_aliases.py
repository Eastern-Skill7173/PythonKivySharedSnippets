from typing import (
    Optional,
    Union,
    TextIO,
    BinaryIO,
)
from pathlib import Path

__all__ = (
    "Number",
    "FilePath",
    "OptionalFilePath",
    "FilePathBytes",
    "TextFileType",
    "BinaryFileType",
)


Number = Union[int, float]
FilePath = Union[str, Path]
OptionalFilePath = Optional[FilePath]
FilePathBytes = Union[FilePath, bytes]
TextFileType = Union[FilePath, TextIO]
BinaryFileType = Union[FilePath, BinaryIO]
