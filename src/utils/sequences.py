import random
from typing import (
    MutableSequence,
    Sequence,
    Iterable,
    Optional,
    Union,
)

__all__ = (
    "shuffle",
    "move_index",
    "replace_index",
    "next_nth_element",
)


def shuffle(
        mutable_sequence: MutableSequence,
        return_copy: bool = True) -> Optional[MutableSequence]:
    """
    Convenience function to shuffle a mutable sequence,
    whether in-place or as a copied sequence
    :param mutable_sequence: The mutable sequence instance to operate on
    :param return_copy: Return copy or shuffle in-place
    :return: Optional[MutableSequence]
    """
    if return_copy:
        sequence_copy = mutable_sequence.copy()
        random.shuffle(sequence_copy)
        return sequence_copy
    else:
        random.shuffle(mutable_sequence)


def move_index(
        list_obj: list,
        element_index: int,
        target_index: int) -> None:
    """
    Convenience function to move an element within a list
    :param list_obj: The list instance to operate on
    :param element_index: The index of the current element to be moved
    :param target_index: The target index to move to
    :return: None
    """
    list_obj.insert(target_index, list_obj.pop(element_index))


def replace_index(
        list_obj: list,
        element_index: int,
        replacement_value) -> None:
    """
    Convenience function to replace an index's element with another value
    :param list_obj: The list instance to operate on
    :param element_index: The index of the element to be replaced
    :param replacement_value: Value to be put in place of the given index
    :return: None
    """
    list_obj.pop(element_index)
    list_obj.insert(element_index, replacement_value)


def next_nth_element(
        sequence: Union[Sequence, Iterable],
        element,
        index_jump: int = 1):
    """
    Convenience function to find the index of
    the given element inside the given sequence
    then return the next `index_jump`th element from
    the same previously given sequence
    :param sequence: Sequence or iterable to find elements from
    :param element: Element to find within the sequence
    :param index_jump: Number of indices to jump for the return value
    """
    try:
        return sequence[sequence.index(element) + index_jump]
    except AttributeError:
        sequence = tuple(sequence)
        return sequence[sequence.index(element) + index_jump]
    except TypeError:
        sequence = tuple(sequence)
        return sequence[sequence.index(element) + index_jump]
