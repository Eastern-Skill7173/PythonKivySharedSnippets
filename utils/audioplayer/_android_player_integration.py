"""
Kivy audio implementation for Android using native API
======================================================
Shoutout to Tito for this snippet (https://github.com/tito)
"""

from jnius import autoclass
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
        return "mp3", "mp4", "aac", "3gp", "flac", "mkv", "wav", "ogg"

    def __init__(self, **kwargs):
        self._mediaplayer = None
        super(AndroidSoundPlayer, self).__init__(**kwargs)

    def load(self):
        self.unload()
        self._mediaplayer = MediaPlayer()
        self._mediaplayer.setAudioStreamType(AudioManager.STREAM_MUSIC)
        self._mediaplayer.setDataSource(self.filename)
        self._mediaplayer.prepare()

    def unload(self):
        self.stop()
        self._mediaplayer = None

    def play(self):
        if not self._mediaplayer:
            return
        self._mediaplayer.start()
        super(AndroidSoundPlayer, self).play()

    def stop(self):
        if not self._mediaplayer:
            return
        self._mediaplayer.reset()

    def seek(self, position):
        if not self._mediaplayer:
            return
        self._mediaplayer.seek(float(position))

    def get_pos(self):
        if self._mediaplayer:
            return self._mediaplayer.getCurrentPosition() / 1000.
        return super(AndroidSoundPlayer, self).get_pos()

    def on_volume(self, instance, volume):
        if self._mediaplayer:
            volume = float(volume)
            self._mediaplayer.setVolume(volume, volume)

    def _get_length(self):
        if self._mediaplayer:
            return self._mediaplayer.getDuration() / 1000.
        return super(AndroidSoundPlayer, self)._get_length()
