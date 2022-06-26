"""
Module is still NOT implemented
"""


from src.constants.app_info import SPOTIFY_DOWNLOADS_DIRECTORY
from src.utils import threaded
from src.utils.audio.streaming_services._base_song import BaseSong

__all__ = (
    "SpotifySong",
)


class SpotifySong(BaseSong):
    """
    Utility class to extract information about a Spotify song
    """

    __slots__ = (
        "_song_id",
        "_downloaded",
    )

    def __init__(self, song_id: str, fetch_info_immediately: bool = True):
        super(SpotifySong, self).__init__()
        self._song_id = song_id
        self._downloaded = False
        if fetch_info_immediately:
            self.fetch_info()

    def __repr__(self) -> str:
        return f"{type(self).__name__}(" \
               f"song_id={self._song_id!r}, " \
               f"downloaded={self._downloaded!r}" \
               f")"

    @threaded
    def fetch_info(self) -> None:
        """
        Method to fetch information related to the audio file.
        (Method can also be called from the user in order
        to re-fetch the information)
        :return: None
        """

    @threaded
    def download(self, silent: bool = False) -> None:
        """
        Method to download to attempt to download the audio file with the given id
        :param silent: Whether to pass exceptions silently or not
        :return: None
        """
        if self._downloaded:
            return
        exception = None
        try:
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
