from typing import Iterable, Union
from kivy.utils import platform
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
from utils import human_readable_duration

__all__ = (
    "AudioPlayer",
)


if platform == "android":
    from _android_player_integration import AndroidSoundPlayer
    SoundLoader.register(AndroidSoundPlayer)


class AudioPlayer:
    """
    Class is still not fully implemented.
    """

    def __init__(self):
        self._state = "no loaded sound"
        self._clock_event = None
        self._current_sound_obj = None

    def load(self, filename) -> None:
        self._current_sound_obj = SoundLoader.load(filename)
        self._state = "sound loaded"

    def unload(self) -> None:
        self._current_sound_obj.unload()
        self._state = "no loaded sound"

    def play(self) -> None:
        self._current_sound_obj.play()
        self._state = "play"

    def stop(self) -> None:
        self._current_sound_obj.stop()
        self._state = "stop"

    def get_pos(self) -> Union[int, float]:
        return self._current_sound_obj.get_pos()

    def seek(self, position: Union[int, float]) -> None:
        self._current_sound_obj.seek(position)

    @property
    def state(self) -> str:
        return self._state
