from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union

# Avoid circular imports for typing.
if TYPE_CHECKING:
    from personality import WalkerPersonality

@dataclass
class TrailSplit:
    """
    A split in the trail.
       _____top______
      /              \
    -<                >-following-
      \____bottom____/
    """

    top: Trail
    bottom: Trail
    following: Trail

    def remove_branch(self) -> TrailStore:
        """Removes the branch, should just leave the remaining following trail."""
        raise NotImplementedError()

@dataclass
class TrailSeries:
    """
    A mountain, followed by the rest of the trail

    --mountain--following--

    """

    mountain: Mountain
    following: Trail

    def remove_mountain(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Removing the mountain at the beginning of this series.
        """
        raise NotImplementedError()

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain in series before the current one.
        """
        raise NotImplementedError()

    def add_empty_branch_before(self) -> TrailStore:
        """Returns a *new* trail which would be the result of:
        Adding an empty branch, where the current trailstore is now the following path.
        """
        raise NotImplementedError()

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain after the current mountain, but before the following trail.
        """
        raise NotImplementedError()

    def add_empty_branch_after(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch after the current mountain, but before the following trail.
        """
        raise NotImplementedError()

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain before everything currently in the trail.
        """
        raise NotImplementedError()

    def add_empty_branch_before(self) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch before everything currently in the trail.
        """
        raise NotImplementedError()

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        raise NotImplementedError()

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""

        mountains = []

        if self.store is None:
            return mountains

        # If the trail is a series
        elif isinstance(self.store, TrailSeries):
            # Add the mountain to the list
            mountains.append(self.store.mountain)
            # Collect all the mountains from the following trail and add them to the list
            mountains.extend(self.store.following.collect_all_mountains())

        # If the trail is a split
        elif isinstance(self.store, TrailSplit):
            mountains.extend(self.store.top.collect_all_mountains())
            mountains.extend(self.store.bottom.collect_all_mountains())
            mountains.extend(self.store.following.collect_all_mountains())


        return mountains

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: 
        # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        """
        Returns a list of lists of mountains which are within the maximum difficulty.
        """
        return self.difficulty_maximum_paths_aux(max_difficulty, [])


    def difficulty_maximum_paths_aux(self, max_difficulty: int, current_path: list[Mountain] = []) -> list[list[Mountain]]:

        # Base Cases
        # If the trail is empty
        if self.store is None:
            # print("store is None")
            return [current_path]

        # Recursive Cases
        # If the trail is a series
        elif isinstance(self.store, TrailSeries):
            if self.store.mountain:
                # If the mountain is within the maximum difficulty
                if self.store.mountain.difficulty_level >= max_difficulty:
                    return []
                current_path.append(self.store.mountain)


            return self.store.following.difficulty_maximum_paths_aux(max_difficulty, current_path)

        # If the trail is a split
        elif isinstance(self.store, TrailSplit):

            # Collect all the paths from the top branch
            top_paths = self.store.top.difficulty_maximum_paths_aux(max_difficulty, current_path.copy())
            bottom_paths = self.store.bottom.difficulty_maximum_paths_aux(max_difficulty, current_path)

            # Add the paths from the bottom branch to the top branch
            paths = top_paths + bottom_paths


            new_paths = []
            for path in paths:
                new_paths.extend(self.store.following.difficulty_maximum_paths_aux(max_difficulty, path))

        return new_paths


