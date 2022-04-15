"""
Not Implemented
"""

from constants import LINUX_PLAYER_SUPPORTED_FILE_EXTENSIONS
from kivy.core.audio import Sound

__all__ = (
    "LinuxSoundPlayer",
)


class LinuxSoundPlayer(Sound):

    @staticmethod
    def extensions():
        return LINUX_PLAYER_SUPPORTED_FILE_EXTENSIONS
