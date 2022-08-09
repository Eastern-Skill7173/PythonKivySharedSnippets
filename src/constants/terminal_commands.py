from typing import Final

__all__ = (
    "SUPPORTED_LINUX_FILE_BROWSERS",
    "SUPPORTED_LINUX_TERMINALS",
)


SUPPORTED_LINUX_FILE_BROWSERS: Final = {
    "plasma": ["dolphin", "--select"],
    "gnome": ["nuatilus", "--select"],
    "zorin": ["nuatilus", "--select"],
}
SUPPORTED_LINUX_TERMINALS: Final = {
    "plasma": ["konsole", "--workdir"],
    "xfce": ["xfce4-terminal", "--default-working-directory"],
    "gnome": ["gnome-terminal", "--working-directory"],
    "zorin": ["gnome-terminal", "--working-directory"]
}
