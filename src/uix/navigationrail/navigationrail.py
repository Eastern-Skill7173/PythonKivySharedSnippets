import os.path
from typing import Final
from src.constants.app_info import UIX_DIRECTORY
from kivy.lang import Builder
from kivy.properties import (
    StringProperty,
    NumericProperty,
    ObjectProperty,
    BooleanProperty
)
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.screenmanager import Screen
from kivymd.uix.behaviors import RectangularElevationBehavior
from src.uix.animations import SnapAnimations
from src.utils import switch_screen

__all__ = (
    "NavigationRailItem",
    "NavigationRail",
)

_DEFAULT_RAIL_SIZE: Final = "90dp"


class NavigationRailItem(ButtonBehavior, BoxLayout):
    icon = StringProperty()
    """
    Icon to be passed to internal `MDIcon` instance.
    
    :attr:`icon` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """
    text = StringProperty()
    """
    Text for the label beneath the `MDIcon` instance.
    
    :attr:`text` is a :class:`~kivy.properties.StringProperty`
    and defaults to `''`.
    """
    selected = BooleanProperty(False)
    """
    Whether the item is selected or not. Internal.
    
    :attr:`selected` is a :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    def __init__(self, **kwargs):
        super(NavigationRailItem, self).__init__(**kwargs)
        self._screen = Screen()

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(icon={self.icon!r}, text={self.text!r}, selected={self.selected!r})"

    def on_release(self):
        self.parent.selected_nav_item = self

    def on_text(self, instance: "NavigationRailItem", text: str) -> None:
        self._screen.name = text

    def on_selected(self, instance: "NavigationRailItem", selected: bool) -> None:
        md_icon = self.ids.md_icon
        md_label = self.ids.md_label
        if selected:
            SnapAnimations.PRIMARY_COLOR.start(md_icon)
            SnapAnimations.PRIMARY_FADE_IN.start(md_label)
        else:
            SnapAnimations.WHITE_COLOR.start(md_icon)
            SnapAnimations.WHITE_FADE_OUT.start(md_label)

    @property
    def screen(self) -> Screen:
        return self._screen

    def add_widget(self, widget, *args, **kwargs):
        if len(self.children) < 2:
            super(NavigationRailItem, self).add_widget(widget, *args, **kwargs)
        else:
            self._screen.add_widget(widget, *args, **kwargs)


class RailItemHolder(RectangularElevationBehavior, GridLayout):
    selected_nav_item = ObjectProperty()
    """
    Currently selected `NavigationRailItem` instance.
    
    :attr:`selected_nav_item` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `None`.
    """
    width = NumericProperty(_DEFAULT_RAIL_SIZE)

    def __init__(self, **kwargs):
        super(RailItemHolder, self).__init__(**kwargs)
        self._previous_screen_name = None

    def on_selected_nav_item(self, instance: "RailItemHolder", selected_nav_item: NavigationRailItem) -> None:
        parent_screen_manager = self.parent.ids.screen_manager
        parent_screen_names = parent_screen_manager.screen_names
        selected_screen_name = selected_nav_item.screen.name
        switch_screen(
            parent_screen_manager,
            selected_screen_name,
            "down" if self._previous_screen_name is not None
            and parent_screen_names.index(selected_screen_name) >
            parent_screen_names.index(self._previous_screen_name) else "up"
        )
        self._previous_screen_name = selected_screen_name

    def _add_screen(self, screen: Screen, name: str) -> None:
        parent_screen_manager = self.parent.ids.screen_manager
        parent_screen_manager.add_widget(screen, index=1)
        screen.unbind(name=self._add_screen)

    def _set_initial_nav_item(self, navigation_rail_item: NavigationRailItem, text: str) -> None:
        self.selected_nav_item = navigation_rail_item
        navigation_rail_item.unbind(text=self._set_initial_nav_item)

    def add_widget(self, widget, *args, **kwargs):
        if not self.children:
            widget.bind(text=self._set_initial_nav_item)
        widget.screen.bind(name=self._add_screen)
        super(RailItemHolder, self).add_widget(widget, *args, **kwargs)


class NavigationRail(BoxLayout):
    rail_width = NumericProperty(_DEFAULT_RAIL_SIZE)
    """
    Width of the side rail.
    
    :attr:`rail_width` is a :class:`~kivy.properties.NumericProperty`
    and defaults to `_DEFAULT_RAIL_SIZE`.
    """
    transition = ObjectProperty(SnapAnimations.SLIDE_TRANSITION)
    """
    Transition for the internal screen manager.
    
    :attr:`transition` is a :class:`~kivy.properties.ObjectProperty`
    and defaults to `SnapAnimations.SLIDE_TRANSITION`
    """

    def add_widget(self, widget, *args, **kwargs):
        if isinstance(widget, NavigationRailItem):
            self.ids.rail_item_holder.add_widget(widget, *args, **kwargs)
        else:
            super(NavigationRail, self).add_widget(widget, *args, **kwargs)


Builder.load_file(
    os.path.join(UIX_DIRECTORY, "navigationrail", "navigationrail_ui.kv")
)
