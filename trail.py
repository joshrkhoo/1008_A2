from __future__ import annotations
from dataclasses import dataclass

from mountain import Mountain

from typing import TYPE_CHECKING, Union

from data_structures.linked_stack import LinkedStack

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
        return TrailSeries(mountain=mountain, # create a new TrailSeries with the first mountain being the new mountain
                           following=Trail(TrailSeries(self.mountain, self.following)) # it is followed by the old TrailSeries
                           ) 

    def add_empty_branch_before(self) -> TrailStore:
        """Returns a *new* trail which would be the result of:
        Adding an empty branch, where the current trailstore is now the following path.
        """
        # first action of the trail now is to split so we should return a TrailSplit
        # top and bottom of the branch will have None as a TrailStore because we're adding an empty branch
        return TrailSplit(top=Trail(None),
                          bottom=Trail(None),
                          following=Trail(TrailSeries(mountain=self.mountain,
                                                      following=self.following)
                                            )
                            )

    def add_mountain_after(self, mountain: Mountain) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding a mountain after the current mountain, but before the following trail.
        """
        return TrailSeries(mountain=self.mountain,
                           following=Trail(TrailSeries(mountain=mountain,
                                                       following=self.following)
                                            )
                            )

    def add_empty_branch_after(self) -> TrailStore:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch after the current mountain, but before the following trail.
        """
        return TrailSeries(mountain=self.mountain,
                           following=Trail(TrailSplit(top=Trail(None),
                                                      bottom=Trail(None),
                                                      following=self.following)
                                            )
                            )

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
                                 following=Trail(self.store)
                                 )
                    )

    def add_empty_branch_before(self) -> Trail:
        """
        Returns a *new* trail which would be the result of:
        Adding an empty branch before everything currently in the trail.
        """
        return Trail(TrailSplit(top=Trail(None),
                                bottom=Trail(None),
                                following=Trail(self.store)
                                )
                    )

    def follow_path(self, personality: WalkerPersonality) -> None:
        """Follow a path and add mountains according to a personality."""
        from personality import PersonalityDecision, TopWalker, BottomWalker, LazyWalker

        current_store = self.store # self is a Trail so self.store will be a TrailSplit, TrailSeries or None
        
        stack = LinkedStack() # use a stack to explore the parts of a split
        # a linked implementation is used rather than an array implementation because we don't know how many splits the trail will have

        while True:
            # if current_store is a TrailSeries, we'll always go through the mountain
            if isinstance(current_store, TrailSeries):
                personality.add_mountain(current_store.mountain)

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
        # could use recursion?

        all_mountains = []

        # base case
        if self.store is None:
            return all_mountains

        elif isinstance(self.store, TrailSeries):
            all_mountains.append(self.store.mountain)
            following_mountains = self.store.following.collect_all_mountains()
            all_mountains.extend(following_mountains)
                

        elif isinstance(self.store, TrailSplit):
            # collect_all_mountains on top trail
            top_mountains = self.store.top.collect_all_mountains()
            # collect_all_mountains on bot trail
            bottom_mountains = self.store.bottom.collect_all_mountains()
            # collect_all_mountains on following trail
            following_mountains = self.store.following.collect_all_mountains()
            all_mountains.extend(top_mountains)
            all_mountains.extend(bottom_mountains)
            all_mountains.extend(following_mountains)
        
        return all_mountains

    def difficulty_maximum_paths(self, max_difficulty: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1008/2085 ONLY!
        raise NotImplementedError()

    def difficulty_difference_paths(self, max_difference: int) -> list[list[Mountain]]: # Input to this should not exceed k > 50, at most 5 branches.
        # 1054 ONLY!
        raise NotImplementedError()
