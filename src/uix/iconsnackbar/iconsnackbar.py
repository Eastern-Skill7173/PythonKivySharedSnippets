import os.path
from src.constants.app_info import UIX_DIRECTORY
from kivy.lang import Builder
from kivy.properties import StringProperty, OptionProperty, NumericProperty
from kivy.clock import mainthread
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

    @mainthread
    def modify_snackbar(self, display_snackbar: bool = False, **kwargs):
        passed_icon_left = kwargs.get("icon_left")
        passed_text = kwargs.get("text")
        passed_font_size = kwargs.get("font_size")
        passed_theme_text_color = kwargs.get("theme_text_color")
        if passed_icon_left:
            self.icon_left = passed_icon_left
        if passed_text:
            self.text = passed_text
        if passed_font_size:
            self.font_size = passed_font_size
        if passed_theme_text_color:
            self.theme_text_color = passed_theme_text_color
        if display_snackbar:
            self.open()


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "iconsnackbar", "iconsnackbar_ui.kv")
)
