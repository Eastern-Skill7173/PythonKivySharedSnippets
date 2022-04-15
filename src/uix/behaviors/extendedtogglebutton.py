from typing import Type
from kivy.properties import BooleanProperty
from kivy.uix.behaviors import ToggleButtonBehavior

__all__ = (
    "ExtendedToggleButtonBehavior",
)


class ExtendedToggleButtonBehavior(ToggleButtonBehavior):
    active = BooleanProperty(False)
    """
    Active value for subclass widgets.

    :attr:`active` is an :class:`~kivy.properties.BooleanProperty`
    and defaults to `False`.
    """

    @classmethod
    def get_active_group_member(cls, group: str) -> Type["ExtendedToggleButtonBehavior"]:
        if group:
            for group_member in cls.get_widgets(group):
                if group_member.active:
                    return group_member
