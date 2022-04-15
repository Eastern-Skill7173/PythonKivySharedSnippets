import os.path
from src.constants.app_info import UIX_DIRECTORY
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView

__all__ = (
    "ScrollBar",
)


class ScrollBar(ScrollView):
    """
    Custom `ScrollView` for more integration with desktop platforms.
    """


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "scrollbar", "scrollbar_ui.kv")
)
