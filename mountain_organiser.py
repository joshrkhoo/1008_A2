from __future__ import annotations

from mountain import Mountain
from algorithms.binary_search import binary_search, _binary_search_aux
from algorithms.mergesort import mergesort, merge


class MountainOrganiser:

    def __init__(self) -> None:
        self.org_mountains = []

    def __str__(self) -> str:
        return str(self.org_mountains)

    def cur_position(self, mountain: Mountain) -> int:
        """
        Return the rank of the mountain given.

        Rank is defined as the position of the mountain in the list of mountains, sorted by difficulty level, then lexicographically by name.
            - sort it by difficulty level
            - if two mountains have the same difficulty level, sort them lexicographically by name
                - return the position of the mountain in the sorted list

        :complexity: Best/Worst case = O(log(N))
            - N is the length of self.org_mountains / the number of mountains in the list of mountains

        """

        # Mountain rank is the position of the mountain in the list of mountains, sorted by difficulty level, then lexicographically by name.
        mountain_rank = binary_search(self.org_mountains, mountain)

        # If the mountain is not in the list of mountains, raise a KeyError
        if self.org_mountains[mountain_rank] == mountain:
            return mountain_rank
        raise KeyError('Mountain does not exist')


    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Add a list of mountains to the list of mountains.

        :complexity: Best/Worst case = O(Mlog(M)+N)
            - M is the number of mountains in self.org_mountains
            - N is the number of mountains in the list of mountains to add
    
        """

        # Sort the list of mountains to add by difficulty level, then lexicographically by name
        sorted_mountains = mergesort(mountains, key=lambda mountain: (mountain.difficulty_level, mountain.name)) 

        # Merge sorted_mountains into self.org_mountains
        self.org_mountains = merge(self.org_mountains, sorted_mountains, key=lambda mountain: (mountain.difficulty_level, mountain.name))
    