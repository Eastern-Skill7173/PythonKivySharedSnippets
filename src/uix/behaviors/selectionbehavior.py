from typing import List
from kivy.lang import Builder
from kivy.properties import (
    BooleanProperty,
    ColorProperty,
    VariableListProperty,
)
from kivy.uix.recycleview.views import RecycleDataViewBehavior

__all__ = (
    "SelectionBehavior",
)


class SelectionBehavior(RecycleDataViewBehavior):
    index = None
    """
    The index of the current item in the recycle-view.
    """
    selected = BooleanProperty(False)
    """
    Whether the instance is selected or not.

    :attr:`selected` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """
    selected_color = ColorProperty()
    """
    Color for the foreground canvas instruction when item is selected.

    :attr:`selected_color` is a :class:`~kivy.properties.ColorProperty`
    and defaults to `[1, 1, 1, 1]`.
    """
    radius = VariableListProperty()
    """
    Radius for the foreground rounded rectangle when selected.

    :attr:`radius` is an :class:`~kivy.properties.VariableListProperty`
    and defaults to `[0, 0, 0, 0]`.
    """

    def refresh_view_attrs(self, rv, index: int, data: List[dict]) -> None:
        self.index = index
        return super(SelectionBehavior, self).\
            refresh_view_attrs(rv, index, data)

    def apply_selection(self, rv, index: int, is_selected: bool) -> None:
        self.selected = is_selected

    def select_instance(self) -> None:
        self.parent.select_node(self.index)  # NOQA

    def deselect_instance(self) -> None:
        self.parent.deselect_node(self.index)  # NOQA

    def select_or_deselect_instance(self) -> None:
        if not self.selected:
            self.select_instance()
        else:
            self.deselect_instance()


Builder.load_string("""
#:kivy 2.1.0
<SelectionBehavior>:
    canvas.after:
        Color:
            rgba: root.selected_color
        RoundedRectangle:
            pos: root.pos
            size: root.size
            radius: root.radius
""")
