from typing import Final
from kivy.animation import Animation
from kivy.uix.screenmanager import SlideTransition
from kivymd.app import MDApp

__all__ = (
    "update_animation",
    "SNAP_ANIM_DURATION",
    "QUICK_ANIM_DURATION",
    "SLOW_ANIM_DURATION",
    "SnapAnimations",
    "QuickAnimations",
    "SlideTransition",
)


def update_animation(animation_obj: Animation, **kwargs) -> None:
    """
    Convenience function to update an already instantiated `Animation`
    object's animated properties
    :param animation_obj: The `Animation` object to be updated
    :param kwargs: List of keyword arguments to update the animated properties
    :return: None
    """
    animation_obj.animated_properties.update(kwargs)


_syscon_app_theme_cls = MDApp.get_running_app().theme_cls
SNAP_ANIM_DURATION: Final = .15
QUICK_ANIM_DURATION: Final = .45
SLOW_ANIM_DURATION: Final = 1
_fade_in_properties = {"opacity": 1}
_fade_out_properties = {"opacity": 0}
_primary_color_properties = {"color": _syscon_app_theme_cls.primary_color}
_white_color_properties = {"color": (1, 1, 1, 1)}


class SnapAnimations:
    """
    Container class for animations with `SNAP_ANIM_DURATION` as their duration
    """
    FADE_IN: Final = Animation(**_fade_in_properties, duration=SNAP_ANIM_DURATION)
    FADE_OUT: Final = Animation(**_fade_out_properties, duration=SNAP_ANIM_DURATION)
    PRIMARY_COLOR: Final = Animation(**_primary_color_properties, duration=SNAP_ANIM_DURATION)
    WHITE_COLOR: Final = Animation(**_white_color_properties, duration=SNAP_ANIM_DURATION)
    WHITE_FADE_OUT: Final = Animation(
        **_white_color_properties,
        **_fade_out_properties,
        duration=SNAP_ANIM_DURATION
    )
    PRIMARY_FADE_IN: Final = Animation(
        **_primary_color_properties,
        **_fade_in_properties,
        duration=SNAP_ANIM_DURATION
    )
    SLIDE_TRANSITION: Final = SlideTransition(duration=SNAP_ANIM_DURATION)


class QuickAnimations:
    """
    Container class for animations with `QUICK_ANIM_DURATION` as their duration
    """
    FADE_IN: Final = Animation(**_fade_in_properties, duration=QUICK_ANIM_DURATION)
    FADE_OUT: Final = Animation(**_fade_out_properties, duration=QUICK_ANIM_DURATION)
    PRIMARY_COLOR: Final = Animation(**_primary_color_properties, duration=QUICK_ANIM_DURATION)
    WHITE_COLOR: Final = Animation(**_white_color_properties, duration=QUICK_ANIM_DURATION)
    WHITE_FADE_OUT: Final = Animation(
        **_white_color_properties,
        **_fade_out_properties,
        duration=QUICK_ANIM_DURATION
    )
    PRIMARY_FADE_IN: Final = Animation(
        **_primary_color_properties,
        **_fade_in_properties,
        duration=QUICK_ANIM_DURATION
    )
    SLIDE_TRANSITION: Final = SlideTransition(duration=QUICK_ANIM_DURATION)


class SlowAnimations:
    """
    Container class for animations with `SLOW_ANIM_DURATION` as their duration
    """
    FADE_IN: Final = Animation(**_fade_in_properties, duration=SLOW_ANIM_DURATION)
    FADE_OUT: Final = Animation(**_fade_out_properties, duration=SLOW_ANIM_DURATION)
    PRIMARY_COLOR: Final = Animation(**_primary_color_properties, duration=SLOW_ANIM_DURATION)
    WHITE_COLOR: Final = Animation(**_white_color_properties, duration=SLOW_ANIM_DURATION)
    WHITE_FADE_OUT: Final = Animation(
        **_white_color_properties,
        **_fade_out_properties,
        duration=SLOW_ANIM_DURATION
    )
    PRIMARY_FADE_IN: Final = Animation(
        **_primary_color_properties,
        **_fade_in_properties,
        duration=SLOW_ANIM_DURATION
    )
    SLIDE_TRANSITION: Final = SlideTransition(duration=SLOW_ANIM_DURATION)
