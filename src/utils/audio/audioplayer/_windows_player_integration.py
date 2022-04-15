"""
Not Implemented
"""

from src.constants.supported_file_extensions import WINDOWS_PLAYER_SUPPORTED_FILE_EXTENSIONS
from kivy.core.audio import Sound

__all__ = (
    "WindowsSoundPlayer",
)


class WindowsSoundPlayer(Sound):

    @staticmethod
    def extensions():
        return WINDOWS_PLAYER_SUPPORTED_FILE_EXTENSIONS
