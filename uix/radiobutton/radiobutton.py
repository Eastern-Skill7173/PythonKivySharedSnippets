import os.path
from constants import UIX_DIRECTORY
from kivy.lang import Builder
from kivy.properties import StringProperty
from uix.behaviors import ExtendedToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout

__all__ = (
    "RadioButton",
)


class RadioButton(ExtendedToggleButtonBehavior, BoxLayout):
    text = StringProperty()
    """
    Text value for the local `Label` instance.
    
    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "radiobutton", "radiobutton_ui.kv")
)
