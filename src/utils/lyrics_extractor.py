"""
Module is NOT tested
"""

import requests.exceptions
import lyrics_extractor
from typing import Optional

__all__ = (
    "LyricsExtractor",
)


class _LyricsSearchResults:
    """
    Private class to handle the search process and its results
    """

    __slots__ = (
        "_title",
        "_lyrics",
        "_silent",
        "_exception",
        "_search_successful",
    )

    def __init__(self, api, song_title: str, silent: bool = True):
        self._title = ''
        self._lyrics = ''
        self._silent = silent
        self._exception = None
        self._search_successful = False
        try:
            self._title, self._lyrics = api.get_lyrics(song_title).values()
            self._search_successful = True
        except requests.exceptions.ConnectionError as \
                requests_connection_error:
            self._exception = requests_connection_error
        except lyrics_extractor.LyricScraperException as \
                lyric_scraper_exception:
            self._exception = lyric_scraper_exception
        if not self._silent and not self._search_successful:
            raise self._exception

    @property
    def title(self) -> str:
        return self._title

    @property
    def lyrics(self) -> str:
        return self._lyrics

    @property
    def exception(self):
        return self._exception

    @property
    def search_successful(self) -> bool:
        return self._search_successful


class LyricsExtractor:
    """
    Utility class to search for the lyrics of a song
    through the given gcs engine-id
    """

    def __init__(
            self,
            gcs_api_key: Optional[str] = None,
            gcs_engine_id: Optional[str] = None) -> None:
        self._gcs_api_key = gcs_api_key
        self._gcs_engine_id = gcs_engine_id
        self._api = None
        self.connect_to_api()

    def connect_to_api(self) -> None:
        """
        Method to connect/reconnect to the API
        :return: None
        """
        if not self._gcs_api_key:
            raise ValueError("API key cannot be empty")
        if not self._gcs_engine_id:
            raise ValueError("Engine ID cannot be empty")
        self._api = lyrics_extractor.SongLyrics(
            self._gcs_api_key,
            self._gcs_engine_id
        )

    def search_lyrics(self, song_title: str) -> _LyricsSearchResults:
        """
        Method to search for the lyrics of the given song title
        :param song_title: Name of the song to search the lyrics of
        :return: _LyricsSearchResults
        """
        return _LyricsSearchResults(self._api, song_title)

    @property
    def gcs_api_key(self) -> str:
        return self._gcs_api_key

    @gcs_api_key.setter
    def gcs_api_key(self, new_gcs_api_key: str) -> None:
        if not isinstance(new_gcs_api_key, str):
            raise TypeError(
                "Cannot set api key to any other type than string"
            )
        if not new_gcs_api_key:
            raise ValueError("API key cannot be empty")
        self._gcs_api_key = new_gcs_api_key

    @property
    def gcs_engine_id(self) -> str:
        return self._gcs_engine_id

    @gcs_engine_id.setter
    def gcs_engine_id(self, new_gcs_engine_id: str) -> None:
        if not isinstance(new_gcs_engine_id, str):
            raise TypeError(
                "Cannot set engine id to any other type than string"
            )
        if not new_gcs_engine_id:
            raise ValueError("Engine ID cannot be empty")
        self._gcs_engine_id = new_gcs_engine_id

    @property
    def api(self):
        return self._api
