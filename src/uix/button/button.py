import os.path
from src.constants.app_info import UIX_DIRECTORY
from kivy.lang import Builder
from kivy.properties import ColorProperty
from kivy.uix.button import Button

__all__ = (
    "FlatButton",
)


class FlatButton(Button):
    active_color = ColorProperty(
        (.5, .5, .5, 1)
    )
    """
    Color for the text when button is clicked (active).

    :attr:`active_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `(.5, .5, .5, 1)`
    """
    normal_color = ColorProperty(
        (1, 1, 1, 1)
    )
    """
    Color for the text when button is not clicked (released).

    :attr:`normal_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `(1, 1, 1, 1)`
    """

    def on_state(self, instance: "FlatButton", state: str) -> None:
        if state == "down":
            self.color = self.active_color
        else:
            self.color = self.normal_color


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "button", "button_ui.kv")
)
