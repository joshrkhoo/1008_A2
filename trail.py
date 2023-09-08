from __future__ import annotations
from dataclasses import dataclass
from data_structures.linked_stack import LinkedStack

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

        # Removes the parrallel trails (branch) and returns the following trail
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
        
        # top is empy 
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
        """Follow a path and add mountains according to a personality."""

        from personality import PersonalityDecision


        current = self.store
        stack = LinkedStack()

        while True:

            # If the current trail is a series 
            if isinstance(current, TrailSeries):
                # Add the mountain to the personality
                personality.add_mountain(current.mountain)
                # Move to the next trail
                current = current.following.store
                
                # If the next trail is empty
                if current is None: 
                    # If the stack is empty, break
                    if stack.is_empty():
                        break
                    # Else, pop the stack and move to the next trail
                    # Pop to get the TrailSplit object from the stack
                    split = stack.pop()
                    current = split.following.store
            

            # If the current trail is a split
            if isinstance(current, TrailSplit):
                # Push the current trail to the stack
                stack.push(current)
                # Get the personality type
                decision = personality.select_branch(current.top, current.bottom)

                # Assign current to the next trail
                if decision == PersonalityDecision.TOP:
                    current = current.top.store
                elif decision == PersonalityDecision.BOTTOM:
                    current = current.bottom.store
                else:
                    break
            
            # If the current trail is empty
            if current is None:
                # Get the next trail object from the stack
                split = stack.pop()
                # update the current to that trail
                current = split.following.store
            

        
              
        

    def collect_all_mountains(self) -> list[Mountain]:
        """Returns a list of all mountains on the trail."""
        raise NotImplementedError()

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        raise NotImplementedError()

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        raise NotImplementedError()
