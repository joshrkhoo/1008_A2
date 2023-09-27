from __future__ import annotations

from mountain import Mountain

from algorithms.binary_search import binary_search, _binary_search_aux, binary_search_mountains, _binary_search_mountains_aux
from algorithms.mergesort import mergesort, merge

class MountainOrganiser:

    def __init__(self) -> None:
        self.organiser = [] # a list of Mountains

    def cur_position(self, mountain: Mountain) -> int:
        """
        Complexity Analysis
        Best Case: The mountain we are looking for is the middle mountain. This results in a complexity of O(1)
        Worst Case: The mountain we are looking for is the very first or last mountain. This results in a complexity of O(log(n)) where n is the number of mountains in the list
        """
        if mountain not in self.organiser: # O(1)
            raise KeyError # O(1)
        
        pos = binary_search_mountains(self.organiser, mountain) # O(binary_search_mountains)
        
        return pos
    

    def add_mountains(self, mountains: list[Mountain]) -> None:
        """
        Complexity Analysis
        Best Case:
        Worst Case:
        """
        # sort mountains
        # merge sorted mountains with self.organiser

        sorted_mountains = mergesort(mountains, key=lambda mountain: (mountain.difficulty_level, mountain.name)) # O(m*log(m)) where m is the number of mountains we're adding
        self.organiser = merge(self.organiser, sorted_mountains, key=lambda mountain: (mountain.difficulty_level, mountain.name)) # O(n) where n is the total number of mountains now (i think)
                                                                                                                                  # because we're combining 2 lists

    
