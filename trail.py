from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain
from data_structures.linked_stack import LinkedStack

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
        return self.following.store

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
        return self.following.store

    def add_mountain_before(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain in series before the current one.
        """
        # Adds a mountain before the current Trail series
        return TrailSeries(mountain=mountain, 
                           following=Trail(TrailSeries(
                               mountain=self.mountain, 
                               following=self.following)))

    def add_empty_branch_before(self) -> TrailStore:
        """Returns a *new* trail which would be the result of:
        Adding an empty branch, where the current trailstore is now the following path.
        """
        # top is empty 
        # bottom is empty
        # following is the current trail
        return TrailSplit(top=Trail(None), 
                          bottom=Trail(None), 
                          following=Trail(TrailSeries(
                              mountain=self.mountain, 
                              following=self.following)))

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain after the current mountain, but before the following trail.
        """
        # current mountain -> new mountain -> following trail
        return TrailSeries(mountain=self.mountain, 
                           following=Trail(TrailSeries(
                               mountain=mountain, 
                               following=self.following)))

    def add_empty_branch_after(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch after the current mountain, but before the following trail.
        """
        # current mountain -> empty branch -> following trail
        return TrailSeries(mountain=self.mountain, 
                           following=Trail(TrailSplit(
                            top=Trail(None), 
                            bottom=Trail(None), 
                            following=self.following)))

TrailStore = Union[TrailSplit, TrailSeries, None]

@dataclass
class Trail:

    store: TrailStore = None

    def add_mountain_before(self, mountain: Mountain) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain before everything currently in the trail.
        """
        return Trail(TrailSeries(mountain=mountain, 
                                 following=self))

    def add_empty_branch_before(self) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch before everything currently in the trail.
        """

        return Trail(TrailSplit(top=Trail(None), 
                                    bottom=Trail(None), 
                                    following=self))

    def follow_path(self, personality: WalkerPersonality) -> None:
        """
        Follow a path and add mountains according to a personality.
        
        :complexity:
        Best/Worst case = O(n)
            - n is the number of trailseries in the path
            - Occurs when no splits are encountered / i.e. the shortest path is taken
        Worst case = O(n+m)
            - n is the number of trailseries
            - m is the number of trailsplits
            - Occurs when encountering a splits / i.e. the longest path is taken
        """

        from personality import PersonalityDecision
        
        # operations are all O(1)
        current_store = self.store # self is a Trail so self.store will be a TrailSplit, TrailSeries or None

        stack = LinkedStack() # use a stack to explore the parts of a split
        # a linked implementation is used rather than an array implementation because we don't know how many splits the trail will have

        while True:
            # if current_store is a TrailSeries, we'll always go through the mountain
            if isinstance(current_store, TrailSeries):
                personality.add_mountain(current_store.mountain) # O(1)
                # now need to update the current_store to the next part of the trail which would be the 'following' part
                current_store = current_store.following.store # Some TrailStore
                # current_store.following is a Trail
                # so current_store.following.store will get the TrailStore which will be a TrailSplit, TrailSeries or None

            if isinstance(current_store, TrailSplit):
                stack.push(current_store)
                decision = personality.select_branch(current_store.top, current_store.bottom)

                if decision == PersonalityDecision.TOP:
                    current_store = current_store.top.store # Some TrailStore
                    # current_store.top is a Trail
                elif decision == PersonalityDecision.BOTTOM:
                    current_store = current_store.bottom.store # Some TrailStore
                    # current_store.bottom is a Trail
                elif decision == PersonalityDecision.STOP:
                    break

            if current_store is None: # we could be at the end of a split or the trail itself
                if stack.is_empty(): # there are no splits at where we are in the trail - we are at the end
                    break
                # we reached the end of a branch in the split
                split = stack.pop()
                current_store = split.following.store # go to the following



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


