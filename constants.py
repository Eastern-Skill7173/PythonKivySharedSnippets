import os.path
from typing import Final
from plyer import storagepath

__all__ = (
    "STARTUP_WIDTH",
    "STARTUP_HEIGHT",
    "UIX_DIRECTORY",
    "IMAGES_DIRECTORY",
    "MUSIC_DIRECTORY",
    "FONTS_DIRECTORY",
    "ICONS_DIRECTORY",
    "ICON_PATH",
    "KILOBYTE",
    "MEGABYTE",
    "GIGABYTE",
    "MINUTE",
    "HOUR",
    "DAY",
    "ROOT_DIRECTORY",
    "USER_HOME_DIRECTORY",
    "USER_DOCUMENTS_DIRECTORY",
    "USER_DOWNLOADS_DIRECTORY",
    "USER_MUSIC_DIRECTORY",
    "USER_PICTURES_DIRECTORY",
    "USER_VIDEOS_DIRECTORY",
)


STARTUP_WIDTH: Final = "800"
STARTUP_HEIGHT: Final = "600"
# Be used with `os.path.join(...)`
UIX_DIRECTORY: Final = "uix"
IMAGES_DIRECTORY: Final = "images"
MUSIC_DIRECTORY: Final = "music"
FONTS_DIRECTORY: Final = "fonts"
ICONS_DIRECTORY: Final = os.path.join(IMAGES_DIRECTORY, "icons")
ICON_PATH: Final = os.path.join(ICONS_DIRECTORY, "icon.png")
KILOBYTE: Final = 1_000
MEGABYTE: Final = KILOBYTE * 1_000
GIGABYTE: Final = MEGABYTE * 1_000
MINUTE: Final = 60
HOUR: Final = MINUTE * 60
DAY: Final = HOUR * 24
ROOT_DIRECTORY: Final = storagepath.get_root_dir()
USER_HOME_DIRECTORY: Final = storagepath.get_home_dir()
USER_DOCUMENTS_DIRECTORY: Final = storagepath.get_documents_dir()
USER_DOWNLOADS_DIRECTORY: Final = storagepath.get_downloads_dir()
USER_MUSIC_DIRECTORY: Final = storagepath.get_music_dir()
USER_PICTURES_DIRECTORY: Final = storagepath.get_pictures_dir()
USER_VIDEOS_DIRECTORY: Final = storagepath.get_videos_dir()
