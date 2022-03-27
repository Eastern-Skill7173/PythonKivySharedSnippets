import os.path
from typing import Final
from constants import UIX_DIRECTORY
from utils import read_json_file
from kivy.utils import platform
from kivy.factory import Factory

__all__ = (
    "TYPOGRAPHY",
)


_DESKTOP_TYPOGRAPHY: Final = read_json_file(
    os.path.join(UIX_DIRECTORY, "desktop_typography.json")
)
_MOBILE_TYPOGRAPHY: Final = read_json_file(
    os.path.join(UIX_DIRECTORY, "mobile_typography.json")
)
_PLATFORM_SPECIFIC_TYPOGRAPHY: Final = {
    "win": _DESKTOP_TYPOGRAPHY,
    "linux": _DESKTOP_TYPOGRAPHY,
    "macosx": _DESKTOP_TYPOGRAPHY,
    "android": _MOBILE_TYPOGRAPHY,
    "ios": _MOBILE_TYPOGRAPHY,
    "unknown": _DESKTOP_TYPOGRAPHY,
}
TYPOGRAPHY: Final = _PLATFORM_SPECIFIC_TYPOGRAPHY[platform]

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
        "MDLogLayout",
        f"{UIX_DIRECTORY}.mdsettingsscreens",
    ),
    (
        "MDInfoLayout",
        f"{UIX_DIRECTORY}.mdsettingsscreens",
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
        "SelectableRecycleBoxLayout",
        f"{UIX_DIRECTORY}.selectablerecyclelayouts",
    ),
    (
        "SelectableRecycleGridLayout",
        f"{UIX_DIRECTORY}.selectablerecyclelayouts",
    ),
    (
        "Separator",
        f"{UIX_DIRECTORY}.separator",
    ),
    (
        "LogLayout",
        f"{UIX_DIRECTORY}.settingsscreens",
    ),
    (
        "InfoLayout",
        f"{UIX_DIRECTORY}.settingsscreens",
    )
):
    Factory.register(classname=class_name, module=module)
