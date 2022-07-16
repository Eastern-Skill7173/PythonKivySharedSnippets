import os.path
from src.constants.app_info import UIX_DIRECTORY
from kivy.lang import Builder
from kivy.properties import StringProperty, OptionProperty, NumericProperty
from kivymd.uix.snackbar import BaseSnackbar

__all__ = (
    "IconSnackBar",
)


class IconSnackBar(BaseSnackbar):
    icon_left = StringProperty()
    """
    Icon value for the left icon on the snack-bar.

    :attr:`icon_left` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """
    text = StringProperty()
    """
    Text value for the snack-bar item.

    :attr:`text` is an :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """
    font_size = NumericProperty("18sp")
    """
    Font size for the internal label.

    :attr:`font_size` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `"18sp"`.
    """
    theme_text_color = OptionProperty(
        "Primary",
        options=[
            "Primary",
            "Secondary",
            "Hint",
            "Error",
            "Custom",
            "ContrastParentBackground",
        ],
    )
    """
    SnackBar's label color scheme name.
    Available options are: `'Primary'`, `'Secondary'`, `'Hint'`, `'Error'`,
    `'Custom'`, `'ContrastParentBackground'`.

    :attr:`theme_text_color` is an :class:`~kivy.properties.OptionProperty`
    and defaults to `"Primary"`.
    """


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "iconsnackbar", "iconsnackbar_ui.kv")
)
