from typing import Final
from plyer import storagepath

__all__ = (
    "ROOT_DIRECTORY",
    "HOME_DIRECTORY",
    "DOCUMENTS_DIRECTORY",
    "DOWNLOADS_DIRECTORY",
    "MUSIC_DIRECTORY",
    "PICTURES_DIRECTORY",
    "VIDEOS_DIRECTORY",
)


ROOT_DIRECTORY: Final = storagepath.get_root_dir()
HOME_DIRECTORY: Final = storagepath.get_home_dir()
DOCUMENTS_DIRECTORY: Final = storagepath.get_documents_dir()
DOWNLOADS_DIRECTORY: Final = storagepath.get_downloads_dir()
MUSIC_DIRECTORY: Final = storagepath.get_music_dir()
PICTURES_DIRECTORY: Final = storagepath.get_pictures_dir()
VIDEOS_DIRECTORY: Final = storagepath.get_videos_dir()
