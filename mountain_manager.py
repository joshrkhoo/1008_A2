from __future__ import annotations
from algorithms.mergesort import mergesort
from mountain import Mountain
from double_key_table import DoubleKeyTable

class MountainManager:

    def __init__(self) -> None:
        self.mountain_manager = DoubleKeyTable()
        self.mountain_manager.hash1 = lambda x: (x % self.mountain_manager.table_size)

    def add_mountain(self, mountain: Mountain) -> None:
        """
        Add the given mountain to the table.
        :complexity: Best/Worst case = O(1)
        """
        key1 = mountain.difficulty_level
        key2 = mountain.name
        self.mountain_manager[key1, key2] = mountain

    def remove_mountain(self, mountain: Mountain) -> None:
        """
        Remove the given mountain from the table.
        :complexity: Best/Worst case = O(1)
        """
        key1 = mountain.difficulty_level
        key2 = mountain.name
        del self.mountain_manager[key1, key2]

    def edit_mountain(self, old: Mountain, new: Mountain) -> None:
        """
        Remove old mountain from the table and add new mountain to the table.
        :complexity: Best/Worst case = O(1)
        """
        self.remove_mountain(old)
        self.add_mountain(new)

    def mountains_with_difficulty(self, diff: int) -> list[Mountain]:
        """
        Return a list of all mountains with the given difficulty level.
        :complexity: Best/Worst case = O(N)
            - N is the number of mountains with the given difficulty level
        """

        list = []

        # If the difficulty level is not in the table, return an empty list
        if diff not in self.mountain_manager.keys():
            return list

        # For each mountain with the given difficulty level, append it to the list
        for mountain in self.mountain_manager.values(diff):
            list.append(mountain)

        return list
