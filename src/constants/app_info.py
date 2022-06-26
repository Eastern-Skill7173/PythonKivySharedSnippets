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
    "STREAMING_SERVICES_DOWNLOADS_DIRECTORY",
    "ICONS_DIRECTORY",
    "ICON_PATH",
    "YOUTUBE_MUSIC_DOWNLOADS_DIRECTORY",
    "SPOTIFY_DOWNLOADS_DIRECTORY",
    "DEEZER_DOWNLOADS_DIRECTORY",
    "SOUNDCLOUD_DOWNLOADS_DIRECTORY",
)


STARTUP_WIDTH: Final = "800"
STARTUP_HEIGHT: Final = "600"
AUDIO_PROVIDER: Final = "ffpyplayer"
# Be used with `os.path.join(...)`
UIX_DIRECTORY: Final = "uix"
IMAGES_DIRECTORY: Final = "images"
MUSIC_DIRECTORY: Final = "music"
FONTS_DIRECTORY: Final = "fonts"
STREAMING_SERVICES_DOWNLOADS_DIRECTORY: Final = "streaming_services_downloads"
ICONS_DIRECTORY: Final = os.path.join(IMAGES_DIRECTORY, "icons")
ICON_PATH: Final = os.path.join(ICONS_DIRECTORY, "icon.png")
YOUTUBE_MUSIC_DOWNLOADS_DIRECTORY: Final = os.path.join(
    STREAMING_SERVICES_DOWNLOADS_DIRECTORY, "youtube_music"
)
SPOTIFY_DOWNLOADS_DIRECTORY: Final = os.path.join(
    STREAMING_SERVICES_DOWNLOADS_DIRECTORY, "spotify"
)
DEEZER_DOWNLOADS_DIRECTORY: Final = os.path.join(
    STREAMING_SERVICES_DOWNLOADS_DIRECTORY, "deezer"
)
SOUNDCLOUD_DOWNLOADS_DIRECTORY: Final = os.path.join(
    STREAMING_SERVICES_DOWNLOADS_DIRECTORY, "soundcloud"
)
