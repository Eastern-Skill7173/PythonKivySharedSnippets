from constants.app_info import (
    STARTUP_WIDTH,
    STARTUP_HEIGHT,
    AUDIO_PROVIDER,
    ICON_PATH,
)
import os

os.environ["KIVY_AUDIO"] = AUDIO_PROVIDER
os.environ["PLATFORM_AUDIO_PLAYER_INTEGRATION"] = "android,windows,linux"

from kivy import Config

Config.set("graphics", "width", STARTUP_WIDTH)
Config.set("graphics", "height", STARTUP_HEIGHT)
Config.set("graphics", "minimum_width", STARTUP_WIDTH)
Config.set("graphics", "minimum_height", STARTUP_HEIGHT)

from kivy.lang import Builder
from kivy.app import App


class MainApp(App):
    def __init__(self, **kwargs):
        super(MainApp, self).__init__(**kwargs)
        self.icon = ICON_PATH
        self.kv = Builder.load_file("main_ui.kv")

    def build(self):
        return self.kv


if __name__ == '__main__':
    MainApp().run()
