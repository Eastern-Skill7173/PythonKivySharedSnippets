import os.path
from constants import UIX_DIRECTORY
from typing import Dict, List
from kivy.lang import Builder
from kivy.properties import StringProperty, BooleanProperty
from kivymd.uix.boxlayout import MDBoxLayout

__all__ = (
    "MDRadioButton",
)


class MDRadioButton(MDBoxLayout):
    groups: Dict[str, List["MDRadioButton"]] = {}
    """
    Holds all defined groups.
    """
    group = StringProperty(None)
    """
    Holds the group value for the local `MDCheckbox` instances.
    
    :attr:`group` is an :class:`~kivy.properties.StringProperty`
    and defaults to `None`.
    """
    active = BooleanProperty(False)
    """
    Active value for the `RadioButton` and local `MDCheckbox` instances.
    
    :attr:`active` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """
    text = StringProperty()
    """
    Text value for the local `MDLabel` instance.
    
    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """

    def on_group(self, instance: "MDRadioButton", group: str) -> None:
        if group not in self.groups:
            self.groups[group] = [instance]
        else:
            self.groups[group].append(instance)

    @classmethod
    def get_active_group_member(cls, group: str) -> "MDRadioButton":
        if group:
            for radio_button in cls.groups[group]:
                if radio_button.active:
                    return radio_button


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "radiobutton", "mdradiobutton_ui.kv")
)
