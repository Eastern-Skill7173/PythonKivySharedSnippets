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
    "TextFileType",
    "BinaryFileType",
)


Number = Union[int, float]
FilePath = Union[str, Path]
OptionalFilePath = Optional[FilePath]
TextFileType = Union[FilePath, TextIO]
BinaryFileType = Union[FilePath, BinaryIO]
