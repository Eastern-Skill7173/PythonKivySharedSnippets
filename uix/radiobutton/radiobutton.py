import os.path
from constants import UIX_DIRECTORY
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivy.uix.behaviors import ToggleButtonBehavior
from kivy.uix.boxlayout import BoxLayout

__all__ = (
    "RadioButton",
)


class RadioButton(ToggleButtonBehavior, BoxLayout):
    active = BooleanProperty(False)
    """
    Active value for the `RadioButton` and local `CheckBox` instances.
    
    :attr:`active` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """
    text = StringProperty()
    """
    Text value for the local `Label` instance.
    
    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    @classmethod
    def get_active_group_member(cls, group: str) -> "RadioButton":
        if group:
            for radio_button in cls.get_widgets(group):
                if radio_button.active:
                    return radio_button


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "radiobutton", "radiobutton_ui.kv")
)
