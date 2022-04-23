"""
Module is still a work in progress
For now it is recommended to not use this module
"""


from typing import Final, Type
from src.type_aliases import Number
from src.constants.uix import (
    SNAP_ANIM_DURATION,
    QUICK_ANIM_DURATION,
    SLOW_ANIM_DURATION,
)
from kivy.animation import Animation
from kivy.uix.screenmanager import (
    TransitionBase,
    SlideTransition,
    FadeTransition,
    CardTransition,
)
from kivymd.app import MDApp
from src.utils import (
    update_animation_duration,
    update_animation_transition,
    update_animation_properties,
)

__all__ = (
    "SNAP_ANIM_DURATION",
    "QUICK_ANIM_DURATION",
    "SLOW_ANIM_DURATION",
    "ExtendedAnimation",
    "SnapAnimations",
    "QuickAnimations",
    "SlowAnimations",
)


_main_app_theme_cls = MDApp.get_running_app().theme_cls
_fade_in_properties = {"opacity": 1}
_fade_out_properties = {"opacity": 0}
_primary_color_properties = {"color": _main_app_theme_cls.primary_color}
_opposite_bg_darkest_color_properties = {"color": _main_app_theme_cls.opposite_bg_darkest}


class ExtendedAnimation(Animation):
    """
    Class extending base `Animation` capabilities,
    allows setting new values for `duration`, `transition`, and `animated_properties` post-initialization.
    """

    def __init__(self, duration: Number = 1, transition: str = "linear", **kwargs):
        self._duration = duration
        self._transition = transition
        self._animated_properties = kwargs
        super(ExtendedAnimation, self).__init__(
            duration=self._duration,
            transition=self._transition,
            **self._animated_properties
        )

    def __repr__(self) -> str:
        return f"{type(self).__name__}(" \
               f"duration={self._duration!r}, " \
               f"transition={self._transition!r}, " \
               f"animated_properties={self.animated_properties!r})"

    def copy(self) -> "ExtendedAnimation":
        """
        Method to return a new `ExtendedAnimation` instance with the same values
        :return: ExtendedAnimation
        """
        return type(self)(self._duration, self._transition, **self._animated_properties)

    def update_animated_properties(self, **kwargs):
        """
        Method to update the animation properties of the instance
        :param kwargs: Key-word arguments to update the animated properties with
        :return: None
        """
        update_animation_properties(self, **kwargs)

    @property
    def duration(self) -> Number:
        return self._duration

    @duration.setter
    def duration(self, new_duration: Number) -> None:
        self._duration = new_duration
        update_animation_duration(self, self._duration)

    @property
    def transition(self) -> str:
        return self._transition

    @transition.setter
    def transition(self, new_transition: str) -> None:
        self._transition = new_transition
        update_animation_transition(self, self._transition)

    @property
    def animated_properties(self) -> dict:
        return self._animated_properties

    @animated_properties.setter
    def animated_properties(self, new_animated_properties: dict) -> None:
        update_animation_properties(self, clear_previous_items=True, **new_animated_properties)


class _BaseAnimContainer:
    """
    Base class for animation containers (`SnapAnimations`, `QuickAnimation`, ...).
    Class is NOT meant to be used on its own
    """
    global_anim_speed: Number = -1
    """
    Global speed for contained animations to be follow.
    Variable is meant to be overwritten only within sub-classes
    and outside of the class should be read-only.
    """

    @staticmethod
    def _check_obj_type(obj) -> None:
        """
        Static-method to check if the given object is of `Animation`
        :param obj: Object to check the type
        :return: None
        """
        if not isinstance(obj, Animation):
            raise TypeError("only instances of Animation are accepted")

    @staticmethod
    def _check_transition_class(transition_class) -> None:
        """
        Static-method to check if the given transition is a subclass of `TransitionBase`
        :param transition_class: Transition class to check its sub-classing
        :return: None
        """
        if not issubclass(transition_class, TransitionBase):
            raise TypeError(f"{transition_class} is not a sub-class of TransitionBase")

    @classmethod
    def _apply_global_speed_anim_duration(cls, anim_obj: Animation) -> None:
        """
        Class-method to ensure that the given animation object's duration
        follows the class level declared global animation speed
        :param anim_obj: The animation object to check duration
        :return: None
        """
        if anim_obj.duration != cls.global_anim_speed:
            if isinstance(anim_obj, Animation):
                update_animation_duration(anim_obj, cls.global_anim_speed)
            elif isinstance(anim_obj, ExtendedAnimation):
                anim_obj.duration = cls.global_anim_speed
            # else:
            #     raise ValueError("given animation's duration does not match the globally declared speed")

    @classmethod
    def _check_anim_obj(cls, anim_obj: Animation) -> None:
        """
        Class-method to apply various checks to the given animation object
        :param anim_obj: The animation object to operate the checks on
        :return: None
        """
        cls._check_obj_type(anim_obj)
        cls._apply_global_speed_anim_duration(anim_obj)

    @classmethod
    def register_animations(cls, **kwargs: Animation) -> None:
        """
        Class-method to add a new animation to be contained within the class
        :param kwargs: Dictionary of keyword arguments to be registered
        :return: None
        """
        for name, anim_obj in kwargs.items():
            cls._check_anim_obj(anim_obj)
            setattr(cls, name, anim_obj)

    @classmethod
    def register_transitions(cls, **kwargs: Type[TransitionBase]) -> None:
        """
        Class-method to add a new transition to be contained within the class
        :param kwargs: Dictionary of keyword arguments to be registered
        :return: None
        """
        for name, transition_class in kwargs.items():
            cls._check_transition_class(transition_class)
            setattr(cls, name, transition_class(duration=cls.global_anim_speed))


class SnapAnimations(_BaseAnimContainer):
    """
    Container class for animations with `SNAP_ANIM_DURATION` as their duration
    """
    global_anim_speed = SNAP_ANIM_DURATION


class QuickAnimations(_BaseAnimContainer):
    """
    Container class for animations with `QUICK_ANIM_DURATION` as their duration
    """
    global_anim_speed = QUICK_ANIM_DURATION


class SlowAnimations(_BaseAnimContainer):
    """
    Container class for animations with `SLOW_ANIM_DURATION` as their duration
    """
    global_anim_speed = SLOW_ANIM_DURATION


_DEFAULT_ANIMATIONS: Final = {
    "FADE_IN": ExtendedAnimation(**_fade_in_properties),
    "FADE_OUT": ExtendedAnimation(**_fade_out_properties),
    "PRIMARY_COLOR": ExtendedAnimation(**_primary_color_properties),
    "OPPOSITE_BG_DARKEST_COLOR": ExtendedAnimation(**_opposite_bg_darkest_color_properties),
    "OPPOSITE_BG_DARKEST_FADE_OUT": ExtendedAnimation(
        **_opposite_bg_darkest_color_properties,
        **_fade_out_properties,
    ),
    "PRIMARY_FADE_IN": ExtendedAnimation(
        **_primary_color_properties,
        **_fade_in_properties,
    ),
}
_DEFAULT_TRANSITION: Final = {
    "FADE_TRANSITION": FadeTransition,
    "SLIDE_TRANSITION": SlideTransition,
    "CARD_TRANSITION": CardTransition,
}

SnapAnimations.register_animations(**_DEFAULT_ANIMATIONS)
SnapAnimations.register_transitions(**_DEFAULT_TRANSITION)
QuickAnimations.register_animations(**_DEFAULT_ANIMATIONS)
QuickAnimations.register_transitions(**_DEFAULT_TRANSITION)
SlowAnimations.register_animations(**_DEFAULT_ANIMATIONS)
SlowAnimations.register_transitions(**_DEFAULT_TRANSITION)
