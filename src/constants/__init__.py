import os
import platform
from typing import Final

__all__ = (
    "AUTHOR_GITHUB_URL",
    "PROJECT_GITHUB_URL",
    "IMAGES_SOURCE_URL",
    "ICONS_SOURCE_URL",
    "FONTS_SOURCE_URL",
    "MUSICS_SOURCE_URL",
    "AUTHOR_GITHUB_SHORT_URL",
    "PROJECT_GITHUB_SHORT_URL",
    "IMAGES_SOURCE_SHORT_URL",
    "ICONS_SOURCE_SHORT_URL",
    "FONTS_SOURCE_SHORT_URL",
    "MUSICS_SOURCE_SHORT_URL",
    "DESKTOP_PLATFORMS",
    "MOBILE_PLATFORMS",
    "CURRENT_MACHINE",
    "DESKTOP_ENVIRONMENT",
)


AUTHOR_GITHUB_URL: Final = "https://github.com/Eastern-Skill7173"
PROJECT_GITHUB_URL: Final = \
    "https://github.com/Eastern-Skill7173/PythonKivySharedSnippets"
IMAGES_SOURCE_URL: Final = "https://unsplash.com/"
ICONS_SOURCE_URL: Final = "https://materialdesignicons.com/"
FONTS_SOURCE_URL: Final = "https://fonts.google.com/"
MUSICS_SOURCE_URL: Final = "https://www.fesliyanstudios.com/"
AUTHOR_GITHUB_SHORT_URL: Final = "github.com/Eastern-Skill7173"
PROJECT_GITHUB_SHORT_URL: Final = \
    "github.com/Eastern-Skill7173/PythonKivySharedSnippets"
IMAGES_SOURCE_SHORT_URL: Final = "unsplash.com"
ICONS_SOURCE_SHORT_URL: Final = "materialdesignicons.com"  # NOQA
FONTS_SOURCE_SHORT_URL: Final = "fonts.google.com"
MUSICS_SOURCE_SHORT_URL: Final = "fesliyanstudios.com"  # NOQA
DESKTOP_PLATFORMS: Final = (
    "win",
    "linux",
    "macosx",
    "unknown",  # Assume unknown operating systems as desktop
)
MOBILE_PLATFORMS: Final = (
    "android",
    "ios",
)
CURRENT_MACHINE: Final = platform.system()
DESKTOP_ENVIRONMENT: Final = os.getenv("DESKTOP_SESSION")
