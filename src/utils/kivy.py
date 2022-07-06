from pathlib import Path
from io import BytesIO
from typing import Optional
from src.type_aliases import Number, FilePathBytes
from src.utils import convert_file_path_to_string
from kivy.logger import LoggerHistory
from kivy.animation import Animation
from kivy.core.image import Image as CoreImage

__all__ = (
    "create_texture",
    "switch_screen",
    "get_logger_history",
    "update_animation_duration",
    "update_animation_transition",
    "update_animation_properties",
)


def create_texture(source: FilePathBytes, extension: str = "jpg"):
    """
    Convenience function to create texture out of bytes
    :param source: Source parameter for the texture. Could be either `str` or `bytes`
    :param extension: File extension to be used for the texture
    :return: Any
    """
    if isinstance(source, (str, Path)):
        with open(convert_file_path_to_string(source), "rb") as file_binary:
            proper_bytes = file_binary.read()
    elif isinstance(source, bytes):
        proper_bytes = source
    else:
        raise TypeError("Invalid type for creating texture")
    return CoreImage(BytesIO(proper_bytes), ext=extension).texture


def switch_screen(screen_manager,
                  screen: str,
                  direction: Optional[str] = None,
                  beginning_transition: Optional = None,
                  ending_transition: Optional = None) -> None:
    """
    Convenience method for switching screens between screen managers
    :param screen_manager: The targeted `ScreenManager` instance
    :param screen: The desired screen to switch to
    :param direction: The direction of `screen_manager` transition
    :param beginning_transition: The transition to use before switching screens
    :param ending_transition: The transition to use after switching screens
    :return: None
    """
    if beginning_transition:
        screen_manager.transition = beginning_transition
    if direction:
        screen_manager.transition.direction = direction
    screen_manager.current = screen
    if ending_transition:
        screen_manager.transition = ending_transition


def get_logger_history() -> str:
    """
    Convenience function to get logger history
    :return: str
    """
    return '\n'.join(log_record.message for log_record in reversed(LoggerHistory.history))


def update_animation_duration(animation_obj: Animation, new_duration: Number) -> None:
    """
    Convenience function to update an `Animation` object's duration
    :param animation_obj: The `Animation` object to be updated
    :param new_duration: New duration to be set for the animation
    :return: None
    """
    animation_obj.__init__(
        duration=new_duration,
        transition=animation_obj.transition,
        **animation_obj.animated_properties
    )


def update_animation_transition(animation_obj: Animation, new_transition: str) -> None:
    """
    Convenience function to update an `Animation` object's transition
    :param animation_obj: The `Animation` object to be updated
    :param new_transition: New transition to be set for the animation
    :return: None
    """
    animation_obj.__init__(
        duration=animation_obj.duration,
        transition=new_transition,
        **animation_obj.animated_properties
    )


def update_animation_properties(
        animation_obj: Animation,
        clear_previous_items: bool = False,
        **kwargs) -> None:
    """
    Convenience function to update an `Animation` object's animated properties
    :param animation_obj: The `Animation` object to be updated
    :param clear_previous_items: Whether to clear the existing properties before updating
    :param kwargs: List of keyword arguments to update the animated properties
    :return: None
    """
    if clear_previous_items:
        animation_obj.animated_properties.clear()
    animation_obj.animated_properties.update(kwargs)
