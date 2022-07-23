"""
Kivy audio implementation for Android using native API
======================================================
Shoutout to Tito for this snippet (https://github.com/tito)
"""

from jnius import autoclass
from src.constants.supported_file_extensions import \
    ANDROID_PLAYER_SUPPORTED_FILE_EXTENSIONS
from kivy.core.audio import Sound

__all__ = (
    "AndroidSoundPlayer",
)


MediaPlayer = autoclass("android.media.MediaPlayer")
FileInputStream = autoclass("java.io.FileInputStream")
AudioManager = autoclass("android.media.AudioManager")


class AndroidSoundPlayer(Sound):

    @staticmethod
    def extensions():
        return ANDROID_PLAYER_SUPPORTED_FILE_EXTENSIONS

    def __init__(self, **kwargs):
        self._media_player = None
        super(AndroidSoundPlayer, self).__init__(**kwargs)

    def load(self):
        self.unload()
        self._media_player = MediaPlayer()
        self._media_player.setAudioStreamType(AudioManager.STREAM_MUSIC)
        self._media_player.setDataSource(self.filename)
        self._media_player.prepare()

    def unload(self):
        self.stop()
        self._media_player = None

    def play(self):
        if not self._media_player:
            return
        self._media_player.start()
        super(AndroidSoundPlayer, self).play()

    def stop(self):
        if not self._media_player:
            return
        self._media_player.reset()

    def seek(self, position):
        if not self._media_player:
            return
        self._media_player.seek(float(position))

    def get_pos(self):
        if self._media_player:
            return self._media_player.getCurrentPosition() / 1000.
        return super(AndroidSoundPlayer, self).get_pos()

    def on_volume(self, instance: "AndroidSoundPlayer", volume):
        if self._media_player:
            volume = float(volume)
            self._media_player.setVolume(volume, volume)

    def _get_length(self):
        if self._media_player:
            return self._media_player.getDuration() / 1000.
        return super(AndroidSoundPlayer, self)._get_length()
