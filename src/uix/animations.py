"""
Module is still a work in progress
For now it is recommended NOT to use this module
"""


from typing import (
    Final,
    Type,
    Union,
    Dict,
    Any,
)
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
    "ExtendedAnimation",
    "BaseAnimContainer",
    "SnapAnimations",
    "QuickAnimations",
    "SlowAnimations",
    "register_default_animations",
    "register_default_transitions",
)


_main_app_theme_cls = MDApp.get_running_app().theme_cls
_fade_in_properties = {"opacity": 1}
_fade_out_properties = {"opacity": 0}
_primary_color_properties = {"color": _main_app_theme_cls.primary_color}
_opposite_bg_darkest_color_properties = {"color": _main_app_theme_cls.opposite_bg_darkest}


def _check_anim_type(anim_obj: Animation) -> None:
    """
    Private function to check if the given object is of Animation
    :param anim_obj: Object to check the type
    :return: None
    """
    if not isinstance(anim_obj, Animation):
        raise TypeError("only instances of Animation are accepted")


def _check_anim_duration(duration: Number) -> None:
    """
    Private function to check if a given duration is of `int` or `float` and is bigger than zero
    :param duration: The duration to apply the checks
    :return: None
    """
    if not isinstance(duration, (int, float)):
        raise TypeError("animation duration can only be an int or a float")
    if duration <= 0:
        raise ValueError("animation duration speed must be more than zero")


def _check_transition_class(transition_class: Type[TransitionBase]) -> None:
    """
    Private function to check if the given transition is a subclass of `TransitionBase`
    :param transition_class: Transition class to check
    :return: None
    """
    if not issubclass(transition_class, TransitionBase):
        raise TypeError(f"{transition_class} is not a sub-class of TransitionBase")


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


class BaseAnimContainer:
    """
    Base class for animation containers (`SnapAnimations`, `QuickAnimation`, ...).
    """

    def __init__(self, global_anim_speed: Number):
        _check_anim_duration(global_anim_speed)
        self._global_anim_speed = global_anim_speed

    def _convert_registration_values_to_anim_objs(
            self,
            anim_obj_or_anim_properties: Union[Dict[str, Any], Animation]) -> Animation:
        """
        Private method to apply checks and convert all registration values to animation objects
        :param anim_obj_or_anim_properties: Animation object or dictionary of animation properties to be converted
        :return: Animation
        """
        if isinstance(anim_obj_or_anim_properties, dict):
            converted_anim_obj = Animation(**anim_obj_or_anim_properties, duration=self._global_anim_speed)
        elif isinstance(anim_obj_or_anim_properties, ExtendedAnimation):
            converted_anim_obj = anim_obj_or_anim_properties.copy()
            converted_anim_obj.duration = self._global_anim_speed
        elif isinstance(anim_obj_or_anim_properties, Animation):
            if anim_obj_or_anim_properties.duration == self._global_anim_speed:
                converted_anim_obj = anim_obj_or_anim_properties
            else:
                raise ValueError(
                    f"{anim_obj_or_anim_properties}'s duration does not match the globally declared anim speed"
                )
        else:
            raise TypeError(f"{anim_obj_or_anim_properties} must be of dict or Animation types")
        return converted_anim_obj

    def register_animations(self, **kwargs: Union[Dict[str, Any], Animation]) -> None:
        """
        Method to add a new animation to be contained within the class
        :param kwargs: Dictionary of keyword arguments to be registered
        :return: None
        """
        for name, anim_obj_or_anim_properties in kwargs.items():
            converted_anim_obj = self._convert_registration_values_to_anim_objs(anim_obj_or_anim_properties)
            self.__dict__[name] = converted_anim_obj

    def register_transitions(self, **kwargs: Type[TransitionBase]) -> None:
        """
        Class-method to add a new transition to be contained within the class
        :param kwargs: Dictionary of keyword arguments to be registered
        :return: None
        """
        for name, transition_class in kwargs.items():
            _check_transition_class(transition_class)
            self.__dict__[name] = transition_class(duration=self._global_anim_speed)

    @property
    def global_anim_speed(self) -> Number:
        return self._global_anim_speed


_DEFAULT_ANIMATIONS: Final = {
    "fade_in": _fade_in_properties,
    "fade_out": _fade_out_properties,
    "primary_color": _primary_color_properties,
    "opposite_bg_darkest_color": _opposite_bg_darkest_color_properties,
    "opposite_bg_darkest_fade_out": {**_opposite_bg_darkest_color_properties, **_fade_out_properties},
    "primary_fade_in": {**_primary_color_properties, **_fade_in_properties},
}
_DEFAULT_TRANSITION: Final = {
    "fade_transition": FadeTransition,
    "slide_transition": SlideTransition,
    "card_transition": CardTransition,
}


def register_default_animations(anim_container: BaseAnimContainer) -> None:
    """
    Convenience function to register default animations to the container
    :param anim_container: Container instance to register the animations to
    :return: None
    """
    anim_container.register_animations(**_DEFAULT_ANIMATIONS)


def register_default_transitions(anim_container: BaseAnimContainer) -> None:
    """
    Convenience function to register default transitions to the container
    :param anim_container: Container class to register the transitions to
    :return: None
    """
    anim_container.register_transitions(**_DEFAULT_TRANSITION)


SnapAnimations = BaseAnimContainer(global_anim_speed=SNAP_ANIM_DURATION)
QuickAnimations = BaseAnimContainer(global_anim_speed=QUICK_ANIM_DURATION)
SlowAnimations = BaseAnimContainer(global_anim_speed=SLOW_ANIM_DURATION)
for pre_defined_anim_container in (SnapAnimations, QuickAnimations, SlowAnimations):
    register_default_animations(pre_defined_anim_container)
    register_default_transitions(pre_defined_anim_container)
