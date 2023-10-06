from __future__ import annotations
from typing import TypeVar

T = TypeVar("T")

def binary_search(l: list[T], item: T) -> int:
    """
    Utilise the binary search algorithm to find the index where a particular element would be stored.

    :return: The index at which either:
        * This item is located, or
        * Where this item would be inserted to preserve the ordering.

    :complexity:
    Best Case Complexity: O(1), when middle index contains item.
    Worst Case Complexity: O(log(N)), where N is the length of l.
    """
    return _binary_search_aux(l, item, 0, len(l))

def _binary_search_aux(l: list[T], item: T, lo: int, hi: int) -> int:
    """
    Auxilliary method used by binary search.
    lo: smallest index where the return value could be.
    hi: largest index where the return value could be.
    """
    if lo == hi:
        return lo
    mid = (hi + lo) // 2
    if l[mid] > item:
        # Item would be before mid
        return _binary_search_aux(l, item, lo, mid-1)
    elif l[mid] < item:
        # Item would be after mid
        return _binary_search_aux(l, item, mid+1, hi)
    elif l[mid] == item:
        return mid
    raise ValueError(f"Comparison operator poorly implemented {item} and {l[mid]} cannot be compared.")


def binary_search_mountains(mountain_list: list[T], mountain: T) -> int:
    """
    Utilise the binary search algorithm to find the index where a particular element would be stored.

    :return: The index at which either:
        * This item is located, or
        * Where this item would be inserted to preserve the ordering.

    :complexity:
    Best Case Complexity: O(1), when middle index contains item.
    Worst Case Complexity: O(log(N)), where N is the length of l.
    """
    return _binary_search_mountains_aux(mountain_list, mountain, 0, len(mountain_list))

def _binary_search_mountains_aux(mountain_list: list[T], mountain: T, lo: int, hi: int) -> int:
    """
    Auxilliary method used by binary search.
    lo: smallest index where the return value could be.
    hi: largest index where the return value could be.
    """
    if lo == hi:
        return lo
    mid = (hi + lo) // 2
    if mountain_list[mid].difficulty_level > mountain.difficulty_level:
        # Item would be before mid
        return _binary_search_mountains_aux(mountain_list, mountain, lo, mid-1)
    elif mountain_list[mid].difficulty_level < mountain.difficulty_level:
        # Item would be after mid
        return _binary_search_mountains_aux(mountain_list, mountain, mid+1, hi)
    elif mountain_list[mid].difficulty_level == mountain.difficulty_level:
        while True:
            if mountain_list[mid].name == mountain.name:
                return mid
            elif mountain_list[mid].name < mountain.name:
                mid += 1
            elif mountain_list[mid].name > mountain.name:
                mid -= 1

    raise ValueError(f"Comparison operator poorly implemented {mountain} and {mountain_list[mid]} cannot be compared.")
