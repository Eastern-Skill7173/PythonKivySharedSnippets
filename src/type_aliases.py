from typing import Optional, Union, TextIO
from pathlib import Path

__all__ = (
    "Number",
    "FilePath",
    "OptionalFilePath",
)


Number = Union[int, float]
FilePath = Union[str, Path]
OptionalFilePath = Optional[FilePath]
