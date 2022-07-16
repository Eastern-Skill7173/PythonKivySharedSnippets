import os.path
from src.constants.app_info import UIX_DIRECTORY
from kivy.lang import Builder
from kivy.properties import StringProperty
from src.uix.behaviors import ExtendedToggleButtonBehavior
from kivymd.uix.boxlayout import MDBoxLayout

__all__ = (
    "MDRadioButton",
)


class MDRadioButton(ExtendedToggleButtonBehavior, MDBoxLayout):
    text = StringProperty()
    """
    Text value for the local `MDLabel` instance.

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "mdradiobutton", "mdradiobutton_ui.kv")
)
