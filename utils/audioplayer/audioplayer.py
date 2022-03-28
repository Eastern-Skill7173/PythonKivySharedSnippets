import os
from typing import Iterable, Union
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from utils import human_readable_duration

__all__ = (
    "AudioPlayer",
)


if platform == "android" and os.getenv("ANDROID_PLAYER_INTEGRATION"):
    from _android_player_integration import AndroidSoundPlayer
    SoundLoader.register(AndroidSoundPlayer)
    """
    In order to utilize android's native media player, before importing the module you
    must set the "ANDROID_PLAYER_INTEGRATION" environmental variable to "True".
    like so:
    
        `import os
        
        os.environ["ANDROID_PLAYER_INTEGRATION"] = "True"
        
        # You must do this before importing the audio player module
        
        from utils.audioplayer import AudioPlayer
        ...
        `
    """


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

    def __init__(self,
                 queue: Iterable[str] = (),
                 volume: Union[int, float] = 1,
                 loop: bool = False,
                 estimate_position: bool = True,
                 interval: Union[int, float] = 1):
        self._external_stop_call = False
        self._queue_progress_index = -1
        self._queue = []
        self.load(*queue)
        self._volume = volume
        self._loop = loop
        self._estimate_position = estimate_position
        self._interval = interval
        self._pos_estimate = 0
        self._human_readable_pos_estimate = human_readable_duration(self._pos_estimate)
        self._state = "queue empty"
        self._clock_event = None
        self._current_sound_obj = None

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(" \
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

    def _update_pos_estimate(self, position: Union[int, float]) -> None:
        """
        Private method to update the position estimate and its human-readable form
        with the given position in seconds
        :param position: New position of the current audio file in seconds
        :return: None
        """
        self._pos_estimate = position
        self._human_readable_pos_estimate = human_readable_duration(self._pos_estimate)

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

    def _advance_in_queue(self, index_jump: int = 1) -> None:
        """
        Method to progress in queue with the given index jump
        :param index_jump: Number of indexes to progress within the queue
        :return: None
        """
        try:
            self._queue_progress_index += index_jump
            self._set_current_sound_obj()
        except IndexError:
            self._queue_progress_index = -1
            if self._loop:
                self._set_current_sound_obj()

    def load(self, *args: Iterable[str]) -> None:
        """
        Method to add audio files to queue
        :param args: List of strings representing individual paths to audio files
        :return: None
        """
        for audio_path in args:
            sound_obj = SoundLoader.load(audio_path)
            sound_obj.volume = self._volume
            sound_obj.bind(
                on_play=lambda sound: self._initialize_estimation()
            )
            sound_obj.bind(
                on_stop=lambda sound: self._cancel_estimation()
            )
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
            self._advance_in_queue()
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

    def get_pos(self) -> Union[int, float]:
        """
        Method to get the position of the current audio file
        :return: Union[int, float]
        """
        return self._current_sound_obj.get_pos()

    def seek(self, position: Union[int, float]) -> None:
        """
        Method to jump to the given position in the current audio file
        :param position: Position to jump to in seconds
        :return: None
        """
        self._current_sound_obj.seek(position)

    def fast_forward(self, seconds: Union[int, float] = 10) -> None:
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

    def rewind(self, seconds: Union[int, float] = 10) -> None:
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
                     stop_current_playback: bool = True,
                     restart_audio_position: bool = True) -> None:
        """
        Method to load the next audio file in the queue
        :param stop_current_playback: Whether to call `self.stop` on the current audio file
        :param restart_audio_position: Whether to reset the position of the current audio file
        :return: None
        """
        if stop_current_playback:
            self.stop()
        self._advance_in_queue()
        if restart_audio_position:
            self.seek(0)
        self.play()

    def skip_to_previous(self,
                         stop_current_playback: bool = True,
                         restart_audio_position: bool = True) -> None:
        """
        Method to load the previous audio file in the queue
        :param stop_current_playback: Whether to call `self.stop` on the current audio file
        :param restart_audio_position: Whether to reset the position of the current audio file
        :return: None
        """
        if stop_current_playback:
            self.stop()
        self._advance_in_queue(-1)
        if restart_audio_position:
            self.seek(0)
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
    def volume(self) -> Union[int, float]:
        return self._volume

    @volume.setter
    def volume(self, new_volume: Union[int, float]) -> None:
        if not isinstance(new_volume, (int, float)):
            raise TypeError("volume can only be an instance of int or float")
        if 0 > new_volume > 1:
            raise ValueError("volume can only be from 0-1")
        self._volume = new_volume
        for sound_obj in self._queue:
            sound_obj.volume = self._volume

    @property
    def pos_estimate(self) -> Union[int, float]:
        return self._pos_estimate

    @property
    def human_readable_pos_estimate(self) -> str:
        return self._human_readable_pos_estimate
