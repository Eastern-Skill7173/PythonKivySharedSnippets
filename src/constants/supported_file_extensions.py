from typing import Final

__all__ = (
    "ANDROID_PLAYER_SUPPORTED_FILE_EXTENSIONS",
    "LINUX_PLAYER_SUPPORTED_FILE_EXTENSIONS",
    "WINDOWS_PLAYER_SUPPORTED_FILE_EXTENSIONS",
)


ANDROID_PLAYER_SUPPORTED_FILE_EXTENSIONS: Final = (
    ".mp3",
    ".mp4",
    ".aac",
    ".3gp",
    ".flac",
    ".mkv",
    ".wav",
    ".ogg",
)
LINUX_PLAYER_SUPPORTED_FILE_EXTENSIONS: Final = (
    ".mp3",
)
WINDOWS_PLAYER_SUPPORTED_FILE_EXTENSIONS: Final = (
    ".mp3",
)
# Currently, given file extensions are dummy ones except android player
