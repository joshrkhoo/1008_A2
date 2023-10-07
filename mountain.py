from __future__ import annotations
from dataclasses import dataclass

@dataclass
class Mountain:

    name: str
    difficulty_level: int
    length: int

    def __gt__(self, other: Mountain) -> bool:
        """
        Return True if this mountain is greater than the other mountain.
        :complexity: Best/Worst case = O(1)
        """
        return (self.difficulty_level, self.name) > (other.difficulty_level, other.name)

    def __lt__(self, other: Mountain) -> bool:
        """
        Return True if this mountain is less than the other mountain.
        :complexity: Best/Worst case = O(1)
        """
        return (self.difficulty_level, self.name) < (other.difficulty_level, other.name)
