"""
Module is still NOT fully implemented
"""


import os.path
from youtube_dl import YoutubeDL
from src.constants.app_info import YOUTUBE_MUSIC_DOWNLOADS_DIRECTORY
from src.utils import (
    threaded,
    human_readable_size,
)
from src.utils.kivy import create_texture
from src.utils.audio.streaming_services.base import BaseSong
from kivy.utils import platform
from kivy.network.urlrequest import UrlRequest

__all__ = (
    "YouTubeMusicSong",
)


def _check_youtube_dl_config_type(youtube_dl_config: YoutubeDL) -> None:
    """
    Private function to check whether the given object is of `YoutubeDL` type
    :param youtube_dl_config: Object to apply checks on
    :return: None
    """
    if not isinstance(youtube_dl_config, YoutubeDL):
        raise TypeError(
            f"youtube_dl configuration can only be of type {YoutubeDL}"
        )


class YouTubeMusicSong(BaseSong):
    """
    Utility class to extract information about a YouTube music song
    """

    _youtube_dl = YoutubeDL(
        {
            "format": "bestaudio/best",
            "outtmpl": os.path.join(
                YOUTUBE_MUSIC_DOWNLOADS_DIRECTORY, "%(title)s.%(ext)s"
            ),
            "nocheckcertificate": platform == "android"
        }
    )

    # FIXME: youtube_dl raises `AttributeError` on android
    # FIXME: youtube_dl cannot verify ssl certificate on android

    __slots__ = (
        "_song_id",
        "_downloaded",
    )

    def __init__(
            self,
            song_id: str,
            fetch_info_immediately: bool = True) -> None:
        super(YouTubeMusicSong, self).__init__()
        self._song_id = song_id
        self._downloaded = False
        if fetch_info_immediately:
            self.fetch_info()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(" \
               f"song_id={self._song_id!r}, " \
               f"downloaded={self._downloaded!r}" \
               f")"

    @classmethod
    def set_youtube_dl_config(cls, youtube_dl_config: YoutubeDL) -> None:
        """
        Class-method to set youtube-dl config obj
        to as the global config when downloading
        :param youtube_dl_config: YouTubeDL configuration obj to apply
        :return: None
        """
        _check_youtube_dl_config_type(youtube_dl_config)
        cls._youtube_dl = youtube_dl_config

    @threaded
    def fetch_info(self) -> None:
        """
        Method to fetch information related to the audio file.
        (Method can also be called from the user in order
        to re-fetch the information)
        :return: None
        """
        try:
            extracted_info = self._youtube_dl.extract_info(
                self._song_id, download=False
            )
            self._path = self._youtube_dl.prepare_filename(extracted_info)
            self._st_size = extracted_info.get("filesize")
            self._file_size = human_readable_size(self._st_size)
            self._title = extracted_info.get("title")
            self._artist = extracted_info.get("uploader")
            self._date = extracted_info.get("upload_date")
            UrlRequest(
                extracted_info.get("thumbnail"),
                on_success=lambda request, result: setattr(
                    self, "_cover", create_texture(result)
                )
            )
        except AttributeError as attribute_error:
            # youtube-dl raises AttributeError on android
            pass

    @threaded
    def download(self, silent: bool = False) -> None:
        """
        Method to download to attempt to download
        the audio file with the given id
        :param silent: Whether to pass exceptions silently or not
        :return: None
        """
        if self._downloaded:
            return
        exception = None
        try:
            self._youtube_dl.download(
                (self._song_id,)
            )
            self._downloaded = True
        except ConnectionError as connection_error:
            exception = connection_error
        if exception and not silent:
            raise exception

    @property
    def song_id(self) -> str:
        return self._song_id

    @property
    def downloaded(self) -> bool:
        return self._downloaded
