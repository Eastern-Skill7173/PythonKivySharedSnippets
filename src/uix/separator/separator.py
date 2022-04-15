import os.path
from src.constants.app_info import UIX_DIRECTORY
from kivy.lang import Builder
from kivy.properties import NumericProperty, ColorProperty
from kivy.uix.widget import Widget

__all__ = (
    "Separator",
)


class Separator(Widget):
    line_thickness = NumericProperty("1dp")
    """
    Thickness of the separator line and the widget's height.
    
    :attr:`line_thickness` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `"1dp"1
    """
    line_color = ColorProperty(
        (.5, .5, .5, 1)
    )
    """
    Color of the separator line.
    
    :attr:`line_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `(.5, .5, .5, 1)`
    """


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "separator", "separator_ui.kv")
)
