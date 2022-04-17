import os.path
from src.constants.app_info import UIX_DIRECTORY
from kivy.lang import Builder
from kivy.uix.recycleview.layout import LayoutSelectionBehavior
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.recyclegridlayout import RecycleGridLayout

__all__ = (
    "SelectableRecycleBoxLayout",
    "SelectableRecycleGridLayout",
)


class SelectableRecycleBoxLayout(LayoutSelectionBehavior, RecycleBoxLayout):
    """Recycle box layout with layout selection behavior."""

    def __repr__(self) -> str:
        return f"{type(self).__name__}(selected_nodes={len(self.selected_nodes)})"


class SelectableRecycleGridLayout(LayoutSelectionBehavior, RecycleGridLayout):
    """Recycle grid layout with layout selection behavior."""

    def __repr__(self) -> str:
        return f"{type(self).__name__}(selected_nodes={len(self.selected_nodes)})"


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "selectablerecyclelayouts", "selectablerecyclelayouts_ui.kv")
)
