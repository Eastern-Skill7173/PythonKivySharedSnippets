from typing import Iterable, Callable

__all__ = (
    "SortedList",
    "NoDuplicateList",
)


def _check_callable(obj: Callable) -> None:
    """
    Checker function to see whether the given object
    has the `__call__` magic method (is callable or not)
    :param obj: Object to check
    :return: None
    """
    if not hasattr(obj, "__call__"):
        raise TypeError(f"{obj} is not callable")


class SortedList(list):
    """
    An always sorted list.
    Sorting happens when a new element is appended or the list is extended.
    `on_sort` event is triggered whenever the list gets sorted
    """

    def __init__(self, iterable: Iterable, on_sort: Callable):
        super(SortedList, self).__init__(iterable)
        _check_callable(on_sort)
        self._on_sort = on_sort
        if not self:
            self.sort()

    def sort(self, *, key, reverse: bool):
        super(SortedList, self).sort(key, reverse)
        self._on_sort()

    def append(self, object):
        super(SortedList, self).append(object)
        self.sort()

    def extend(self, iterable: Iterable):
        super(SortedList, self).extend(iterable)
        self.sort()

    def __setitem__(self, i, o):
        super(SortedList, self).__setitem__(i, o)
        self.sort()

    @property
    def on_sort(self):
        return self._on_sort

    @on_sort.setter
    def on_sort(self, new_on_sort: Callable) -> None:
        _check_callable(new_on_sort)
        self._on_sort = new_on_sort


class NoDuplicateList(list):
    """
    A list, not allowing duplicates.
    `on_duplicate` event is triggered whenever a duplicate is found in the list
    """

    def __init__(self, iterable: Iterable, on_duplicate: Callable):
        super(NoDuplicateList, self).__init__(iterable)
        _check_callable(on_duplicate)
        self._on_duplicate = on_duplicate

    def _check_duplication(self, element) -> bool:
        """
        Convenience/Semantic method to check
        if the given element is already in the list
        :param element: Element to check if it is a duplicate
        :return: bool
        """
        return element in self

    def _generate_clean_iterable(self, iterable: Iterable):
        """
        Convenience function to loop over an iterable
        and filter out the contained duplicates
        :param iterable: The iterable to clean (filter out duplicates)
        :returns: generator
        """
        return (
            element for element in iterable
            if not self._check_duplication(element)
        )

    def append(self, element, on_duplicate: Callable):
        if not self._check_duplication(element):
            super(NoDuplicateList, self).append(element)
        else:
            on_duplicate()

    def extend(self, iterable: Iterable):
        no_duplicate_list = self._generate_clean_iterable(iterable)
        super(NoDuplicateList, self).extend(no_duplicate_list)

    def __setitem__(self, i, o):
        checked_obj = None
        if type(i, slice) and hasattr(o, "__iter__"):
            checked_obj = self._generate_clean_iterable(o)
        elif not self._check_duplication(o):
            checked_obj = o
        else:
            raise ValueError(f"{o} is already in the list")
        super(NoDuplicateList, self).__setitem__(i, checked_obj)

    @property
    def on_duplicate(self):
        return self._on_duplicate

    @on_duplicate.setter
    def on_duplicate(self, new_on_duplicate: Callable):
        _check_callable(new_on_duplicate)
        self._on_duplicate = new_on_duplicate
