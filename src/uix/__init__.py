import os.path
from typing import Final
from src.constants.app_info import UIX_DIRECTORY, TYPOGRAPHY_DIRECTORY
from kivy.utils import platform
from kivy.factory import Factory
from src.uix._typography import TypoGraphy

__all__ = (
    "AppTypoGraphy",
)


_DESKTOP_TYPOGRAPHY_PATH: Final = os.path.join(
    TYPOGRAPHY_DIRECTORY, "_desktop_typography.json"
)
_MOBILE_TYPOGRAPHY_PATH: Final = os.path.join(
    TYPOGRAPHY_DIRECTORY, "_mobile_typography.json"
)
_PLATFORM_SPECIFIC_TYPOGRAPHY_PATH: Final = {
    "win": _DESKTOP_TYPOGRAPHY_PATH,
    "linux": _DESKTOP_TYPOGRAPHY_PATH,
    "macosx": _DESKTOP_TYPOGRAPHY_PATH,
    "android": _MOBILE_TYPOGRAPHY_PATH,
    "ios": _MOBILE_TYPOGRAPHY_PATH,
    "unknown": _DESKTOP_TYPOGRAPHY_PATH,
}
AppTypoGraphy = TypoGraphy(
    json_typography_path=_PLATFORM_SPECIFIC_TYPOGRAPHY_PATH[platform]
)

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
