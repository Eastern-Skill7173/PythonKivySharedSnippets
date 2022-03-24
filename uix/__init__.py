from typing import Final
from constants import UIX_DIRECTORY
from kivy.metrics import sp
from kivy.factory import Factory

__all__ = (
    "TYPOGRAPHY",
)


TYPOGRAPHY: Final = {
    "secondary-label": sp(18),
}

for class_name, module in (
    (
        "FlatButton",
        f"{UIX_DIRECTORY}.button",
    ),
    (
        "IconSnackBar",
        f"{UIX_DIRECTORY}.iconsnackbar",
    ),
    (
        "MDRadioButton",
        f"{UIX_DIRECTORY}.mdradiobutton",
    ),
    (
        "NavigationRailItem",
        f"{UIX_DIRECTORY}.navigationrail",
    ),
    (
        "NavigationRail",
        f"{UIX_DIRECTORY}.navigationrail",
    ),
    (
        "RadioButton",
        f"{UIX_DIRECTORY}.radiobutton",
    ),
    (
        "ScrollBar",
        f"{UIX_DIRECTORY}.scrollbar",
    ),
    (
        "Separator",
        f"{UIX_DIRECTORY}.separator",
    ),
):
    Factory.register(classname=class_name, module=module)
