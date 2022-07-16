import os.path
from src.constants.app_info import UIX_DIRECTORY
from src.constants.uix import TOMATO_RGB
from kivy.lang import Builder
from kivy.properties import ColorProperty, StringProperty
from kivymd.uix.boxlayout import MDBoxLayout

__all__ = (
    "MDLogLayout",
    "MDInfoLayout",
)


class MDLogLayout(MDBoxLayout):
    logger_history = StringProperty()
    """
    Output of kivy's logging.

    :attr:`logger_history` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`
    """
    warning_note_color = ColorProperty(TOMATO_RGB)
    """
    Warning color for the `NOTE:` portion of the labels.

    :attr:`warning_note_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `TOMATO_RGB`
    """
    _instance = None

    def __new__(cls, *args, **kwargs):
        """
        These widgets are meant to be initialized just once
        """
        if cls._instance is None:
            cls._instance = super(MDLogLayout, cls).__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):
        super(MDLogLayout, self).__init__(**kwargs)
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


class MDInfoLayout(MDBoxLayout):
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
            cls._instance = super(MDInfoLayout, cls).__new__(cls)
        return cls._instance


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "mdsettingsscreens", "mdsettingsscreens_ui.kv")
)
