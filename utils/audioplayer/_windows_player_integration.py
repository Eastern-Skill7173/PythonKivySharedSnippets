"""
Not Implemented
"""

from constants import WINDOWS_PLAYER_SUPPORTED_FILE_EXTENSIONS
from kivy.core.audio import Sound

__all__ = (
    "WindowsSoundPlayer",
)


class WindowsSoundPlayer(Sound):

    @staticmethod
    def extensions():
        return WINDOWS_PLAYER_SUPPORTED_FILE_EXTENSIONS
