"""
Module is still a work in progress
For now it is recommended NOT to use this module
"""


import os
from pathlib import Path
from typing import Iterable, Union, Final
from src.type_aliases import Number, FilePath
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.audio import SoundLoader, Sound
from src.utils import human_readable_duration, convert_file_path_to_string

__all__ = (
    "AudioPlayer",
)


# TODO: integrate player with windows and linux as well
if platform in os.getenv("PLATFORM_AUDIO_PLAYER_INTEGRATION", '').split(','):
    if platform == "android":
        from _android_player_integration import AndroidSoundPlayer
        SoundLoader.register(AndroidSoundPlayer)
    elif platform == "linux":
        from _linux_player_integration import LinuxSoundPlayer
        SoundLoader.register(LinuxSoundPlayer)
    elif platform == "win":
        from _windows_player_integration import WindowsSoundPlayer
        SoundLoader.register(WindowsSoundPlayer)

"""
In order to integrate and utilize every platform's native media player,
before importing the module you must set the "PLATFORM_AUDIO_PLAYER_INTEGRATION"
environmental variable to a list of platforms separated with a comma.
As an example, to integrate the player with android and windows:

    import os

    os.environ["PLATFORM_AUDIO_PLAYER_INTEGRATION"] = "android,windows"

    # You must do this before importing the audio player module

    from utils.audioplayer import AudioPlayer
    ...

Currently supported platforms are:
    android: `android`

Soon to be integrated:
    windows: `win`
    linux: `linux`
"""


def _convert_registration_value_to_sound_objs(filepath_or_sound_obj: Union[FilePath, Sound]) -> Sound:
    """
    Private function to check & convert registration value to sound objects
    :param filepath_or_sound_obj: Path or sound object at registration to be converted
    :return: Sound
    """
    if isinstance(filepath_or_sound_obj, (str, Path)):
        sound_obj = SoundLoader.load(convert_file_path_to_string(filepath_or_sound_obj))
    elif isinstance(filepath_or_sound_obj, Sound):
        sound_obj = filepath_or_sound_obj
    else:
        raise TypeError("can only accept types of str, Path and Sound")
    return sound_obj


class AudioPlayer:
    """
    Audio player class for extending standard `SoundLoader` functionalities including:
    queuing, fast forwarding, rewinding, global volume, extended states...
    This class has the most integration with ffmpeg & the `ffpyplayer` package.
    In order to switch your audio provider, check out:
    https://kivy.org/doc/stable/guide/environment.html#restrict-core-to-specific-implementation

    BUG:
        In kivy 2.1.0, calling `.stop()` on an audio file and then `.play()`
        causes audio to restart from beginning. When tested on 2.0.0, the error
        was not there.
    """
    _ALLOWED_CLASSES: Final = (Sound, str)
    """
    Private tuple of allowed classes
    to check types when registering a new alias
    """
    _aliases = {}
    """
    Private dictionary containing aliases
    """

    def __init__(self,
                 queue: Iterable = (),
                 volume: Number = 1,
                 loop: bool = False,
                 estimate_position: bool = True,
                 interval: Number = 1):
        self._external_stop_call = False
        self._queue_progress_index = -1
        self._queue = []
        self._volume = volume
        self.load(*queue)
        self._loop = loop
        self._estimate_position = estimate_position
        self._interval = interval
        self._pos_estimate = 0
        self._state = "queue empty"
        self._clock_event = None
        self._current_sound_obj = None

    def __repr__(self) -> str:
        return f"{type(self).__name__}(" \
               f"remaining_in_queue={self.__len__()!r}, " \
               f"loop={self._loop!r}, " \
               f"estimate_position={self._estimate_position!r}, " \
               f"interval={self._interval!r})"

    def __iter__(self):
        for sound_obj in self._queue[self._queue_progress_index + 1:]:
            yield sound_obj

    def __len__(self) -> int:
        return len(self._queue[self._queue_progress_index + 1:])

    def __contains__(self, item) -> bool:
        return item in self._queue[self._queue_progress_index + 1:]

    @classmethod
    def aliases(cls) -> dict:
        """
        Class-method to return the currently registered aliases
        :return: dict
        """
        return cls._aliases.copy()

    @classmethod
    def register(cls, alias, value) -> None:
        """
        Class-method to register a sound object or a string as an easily accessible alias
        :param alias: Alias to be used for the value
        :param value: The value to be registered with the given alias
        :return: None
        """
        cls._check_obj_type(value)
        cls._aliases[alias] = value

    @classmethod
    def _check_obj_type(cls, obj) -> None:
        """
        Private class-method to check if an object is of the allowed types
        :param obj: Object to be checked
        :return: None
        """
        if not isinstance(obj, cls._ALLOWED_CLASSES):
            raise TypeError(f"object can only be either {cls._ALLOWED_CLASSES!r}")

    @classmethod
    def get_alias(cls, alias, default_value=None):
        """
        Class-method to get a registered alias value
        :param alias: Alias that is registered with the value
        :param default_value: Value to return if the given alias could not be found
        :return: Any
        """
        return cls._aliases.get(alias, default_value)

    def _normalize_index(self, index: int) -> int:
        """
        Private method to convert a reverse index to a standard one
        :param index: Index to be checked then converted
        :return: int
        """
        return len(self._queue) + index if index < 0 else index

    def _update_pos_estimate(self, position: Number) -> None:
        """
        Private method to update the position estimate with the given position in seconds
        :param position: New position of the current audio file in seconds
        :return: None
        """
        self._pos_estimate = position

    def _cancel_clock(self) -> None:
        """
        Method to cancel `self._clock_event`
        :return: None
        """
        self._clock_event.cancel()

    def _start_clock(self) -> None:
        """
        Method to start a clock for updating the position estimate
        every `self._interval`
        :return: None
        """
        self._clock_event = Clock.schedule_interval(
            lambda dt: self._update_pos_estimate(self._pos_estimate + self._interval),
            self._interval
        )

    def _initialize_estimation(self) -> None:
        """
        Method to be bound to every sound object's `on_play` event
        to initialize the clock for position estimation if enabled
        :return: None
        """
        if self._estimate_position:
            self._start_clock()

    def _cancel_estimation(self) -> None:
        """
        Method to be bound to every sound object's `on_stop` event
        to cancel the clock to prevent inaccurate position estimation if enabled
        :return: None
        """
        if self._estimate_position:
            self._cancel_clock()
        if not self._external_stop_call:
            self._update_pos_estimate(0)
            self.skip_to_next(stop_current_playback=False)

    def _set_current_sound_obj(self) -> None:
        """
        Method to set the current sound object to the queue progression element
        retrieved using its index from the queue
        :return: None
        """
        self._current_sound_obj = self._queue[self._queue_progress_index]

    def _jump_to_index(self, index: int) -> None:
        """
        Method to jump to the given index in the queue
        :param index: Index of the queue to jump to
        :return: None
        """
        try:
            self._queue_progress_index = index
            self._set_current_sound_obj()
        except IndexError:
            self._queue_progress_index = -1
            self._current_sound_obj = None
            if self._loop:
                self.play()

    def _configure_sound_obj(self, sound_obj: Sound) -> None:
        """
        Private method to configure a sound object to match player behavior.
        (Set its volume to globally declared volume, Bind `on_play` & `on_stop` methods...)
        :param sound_obj: The sound object to be configured
        :return:
        """
        sound_obj.volume = self._volume
        sound_obj.bind(
            on_play=lambda sound: self._initialize_estimation()
        )
        sound_obj.bind(
            on_stop=lambda sound: self._cancel_estimation()
        )

    def clear_queue(self) -> None:
        """
        Method to clear what is in the queue
        :return: None
        """
        self._queue.clear()

    def load(self,
             *args: Union[str, Sound],
             clear_previous_queue: bool = False,
             ignore_aliases: bool = False) -> None:
        """
        Method to add audio files to queue
        :param args: List of strings representing individual paths to audio files
        or pre-initialized sound objects
        :param clear_previous_queue: Clear whatever is in the queue before loading new files
        :param ignore_aliases: Whether to avoid fetching given values from registered aliases
        :return: None
        """
        if clear_previous_queue:
            self.clear_queue()
        for audio_file in args:
            if not ignore_aliases:
                found_alias = self.get_alias(audio_file)
                if found_alias:
                    audio_file = found_alias
            sound_obj = _convert_registration_value_to_sound_objs(audio_file)
            self._configure_sound_obj(sound_obj)
            self._queue.append(sound_obj)
        if self._queue:
            self._state = "queue loaded"

    def unload(self) -> None:
        """
        Method to de-activate and shutdown the audio player
        :return: None
        """
        if self._current_sound_obj:
            self._current_sound_obj.unload()
        self._queue.clear()
        self._state = "queue empty"

    def play(self) -> None:
        """
        Method to start playing the current audio file.
        If none, then advance in queue to load the next
        :return: None
        """
        if not self._current_sound_obj:
            self._jump_to_index(0)
        self._current_sound_obj.play()
        self._state = "play"

    def stop(self) -> None:
        """
        Method to pause the current audio file.
        This method will set `self._external_stop_call` to `True`
        when called to indicate that the stopping was from the wrapper class
        :return: None
        """
        self._external_stop_call = True
        self._current_sound_obj.stop()
        self._state = "stop"
        self._external_stop_call = False

    def get_pos(self) -> Number:
        """
        Method to get the position of the current audio file
        :return: Number
        """
        return self._current_sound_obj.get_pos()

    def seek(self, position: Number) -> None:
        """
        Method to jump to the given position in the current audio file
        :param position: Position to jump to in seconds
        :return: None
        """
        self._current_sound_obj.seek(position)

    def fast_forward(self, seconds: Number = 10) -> None:
        """
        Method to skip the next given seconds in the current audio file
        :param seconds: Jump/Skip duration in seconds
        :return:
        """
        current_song_position = self.get_pos()
        current_song_length = self.length
        if current_song_length - current_song_position > seconds:
            new_position = current_song_position + seconds
        else:
            new_position = current_song_length
        self.seek(new_position)
        if self._estimate_position:
            self._update_pos_estimate(new_position)

    def rewind(self, seconds: Number = 10) -> None:
        """
        Method to go back in the next given seconds in the current audio file
        :param seconds: Duration to rewind/jump back to in seconds
        :return: None
        """
        current_song_position = self.get_pos()
        if current_song_position > seconds:
            new_position = current_song_position - seconds
        else:
            new_position = 0
        self.seek(new_position)
        if self._estimate_position:
            self._update_pos_estimate(new_position)

    def skip_to_next(self,
                     play_immediately: bool = True,
                     stop_current_playback: bool = True,
                     restart_audio_position: bool = True) -> None:
        """
        Method to load the next audio file in the queue
        :param play_immediately: Whether to play the next track immediately or just load it
        :param stop_current_playback: Whether to call `self.stop` on the current audio file
        :param restart_audio_position: Whether to reset the position of the current audio file
        :return: None
        """
        if stop_current_playback:
            self.stop()
        self._jump_to_index(self._queue_progress_index + 1)
        if restart_audio_position:
            self.seek(0)
        if play_immediately:
            self.play()

    def skip_to_previous(self,
                         play_immediately: bool = True,
                         stop_current_playback: bool = True,
                         restart_audio_position: bool = True) -> None:
        """
        Method to load the previous audio file in the queue
        :param play_immediately: Whether to play the previous track immediately or just load it
        :param stop_current_playback: Whether to call `self.stop` on the current audio file
        :param restart_audio_position: Whether to reset the position of the current audio file
        :return: None
        """
        if stop_current_playback:
            self.stop()
        self._jump_to_index(
            self._normalize_index(self._queue_progress_index - 1)
        )
        if restart_audio_position:
            self.seek(0)
        if play_immediately:
            self.play()

    @property
    def queue_progress_index(self) -> int:
        return self._queue_progress_index

    @property
    def state(self) -> str:
        return self._state

    @property
    def source(self) -> str:
        return self._current_sound_obj.source

    @property
    def length(self) -> float:
        return self._current_sound_obj.length

    @property
    def human_readable_length(self) -> str:
        return human_readable_duration(self.length)

    @property
    def volume(self) -> Number:
        return self._volume

    @volume.setter
    def volume(self, new_volume: Number) -> None:
        if not isinstance(new_volume, (int, float)):
            raise TypeError("volume can only be an instance of int or float")
        if 0 > new_volume > 1:
            raise ValueError("volume can only be from 0-1")
        self._volume = new_volume
        for sound_obj in self._queue:
            sound_obj.volume = self._volume

    @property
    def pos_estimate(self) -> Number:
        return self._pos_estimate

    @property
    def human_readable_pos_estimate(self) -> str:
        return human_readable_duration(self._pos_estimate)
