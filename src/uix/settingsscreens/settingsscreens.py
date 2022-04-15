import os.path
from src.constants.app_info import UIX_DIRECTORY
from kivy.lang import Builder
from kivy.properties import ColorProperty, StringProperty
from kivy.uix.boxlayout import BoxLayout

__all__ = (
    "LogLayout",
    "InfoLayout",
)


class LogLayout(BoxLayout):
    logger_history = StringProperty()
    """
    Output of kivy's logging.
    
    :attr:`logger_history` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`
    """
    warning_note_color = ColorProperty(
        [1, 0.38823529411764707, 0.2784313725490196]
    )
    """
    Warning color for the `NOTE:` portion of the labels.
    
    :attr:`warning_note_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[1, 0.38823529411764707, 0.2784313725490196]`
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        These widgets are meant to be initialized just once
        """
        if cls._instance is None:
            cls._instance = super(LogLayout, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        super(LogLayout, self).__init__(**kwargs)
        self.register_event_type("on_save_changes")
        self.register_event_type("on_save_log")

    def on_save_changes(self, button) -> None:
        """
        Dummy method for registering 'on_save_changes' event type
        :param button: Button instance that triggers the event
        :return: None
        """

    def on_save_log(self, button) -> None:
        """
        Dummy method for registering 'on_save_log' event type
        :param button: Button instance that triggers the event
        :return: None
        """


class InfoLayout(BoxLayout):
    application_name = StringProperty()
    """
    Name of the application.
    
    :attr:`application_name` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """
    software_version = StringProperty("0.0.1")
    """
    Current version of the software.
    
    :attr:`software_version` is a :class:`~kivy.properties.StringProperty`
    and defaults to `"0.0.1"`.
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        These widgets are meant to be initialized just once
        """
        if cls._instance is None:
            cls._instance = super(InfoLayout, cls).__new__(cls)
        return cls._instance


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "settingsscreens", "settingsscreens_ui.kv")
)
