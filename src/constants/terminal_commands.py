from typing import Final

__all__ = (
    "SUPPORTED_LINUX_FILE_BROWSERS",
)


SUPPORTED_LINUX_FILE_BROWSERS: Final = {
    "plasma": ["dolphin", "--select"],
    "gnome": ["nuatilus", "--select"],
    "zorin": ["nuatilus", "--select"],
}
