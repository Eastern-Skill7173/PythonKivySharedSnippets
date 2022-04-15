import os.path
from typing import Final

__all__ = (
    "STARTUP_WIDTH",
    "STARTUP_HEIGHT",
    "AUDIO_PROVIDER",
    "UIX_DIRECTORY",
    "IMAGES_DIRECTORY",
    "MUSIC_DIRECTORY",
    "FONTS_DIRECTORY",
    "ICONS_DIRECTORY",
    "ICON_PATH",
)


STARTUP_WIDTH: Final = "800"
STARTUP_HEIGHT: Final = "600"
AUDIO_PROVIDER: Final = "ffpyplayer"
# Be used with `os.path.join(...)`
UIX_DIRECTORY: Final = "uix"
IMAGES_DIRECTORY: Final = "images"
MUSIC_DIRECTORY: Final = "music"
FONTS_DIRECTORY: Final = "fonts"
ICONS_DIRECTORY: Final = os.path.join(IMAGES_DIRECTORY, "icons")
ICON_PATH: Final = os.path.join(ICONS_DIRECTORY, "icon.png")
