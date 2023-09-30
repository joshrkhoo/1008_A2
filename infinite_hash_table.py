from __future__ import annotations
from typing import Generic, TypeVar

from data_structures.referential_array import ArrayR

K = TypeVar("K")
V = TypeVar("V")

class InfiniteHashTable(Generic[K, V]):
    """
    Infinite Hash Table.

    Type Arguments:
        - K:    Key Type. In most cases should be string.
                Otherwise `hash` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    TABLE_SIZE = 27




    def __init__(self, level: int = 0) -> None:
        self.level = level
        self.table = [None] * self.TABLE_SIZE
        self.count = 0

    def hash(self, key: K) -> int:
        if self.level < len(key):
            return ord(key[self.level]) % (self.TABLE_SIZE-1)
        return self.TABLE_SIZE-1


    def __getitem__(self, key: K) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        
        pos = self.hash(key)

        item = self.table[pos]

        if item is None:
            raise KeyError('Key does not exist')

        if isinstance(item, InfiniteHashTable):
            return item[key]

        if item[0] == key:
            return item[1]


    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """

        pos = self.hash(key)

        # This is if we have an empty slot
        if self.table[pos] is None:
            self.table[pos] = (key, value)
            self.count += 1
            return

        # This is if we have a sub table
        if isinstance(self.table[pos], InfiniteHashTable):
            self.table[pos][key] = value
            self.count += 1
            return

        # Found the key, just update the value
        if self.table[pos][0] == key:
            self.table[pos] = (key, value)
            return
    
        # This is if we have a conflict
        conflict_key, conflict_value = self.table[pos]

            # Create sub table at the current position
                # this is where the conflict is currently stored
                    # Essentially we are moving the conflict down a level by deleting it and adding it to the sub table
        self.table[pos] = InfiniteHashTable(
            level=self.level+1
        )
        next_level_table = self.table[pos]
            # Add both keys in the conflict to the sub table
        next_level_table[key] = value
        self.count += 1
        next_level_table[conflict_key] = conflict_value


    def __delitem__(self, key: K) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        pos = self.hash(key)

        item = self.table[pos]

        if item is None:
            raise KeyError('Key does not exist')

        if isinstance(item, InfiniteHashTable):
            # delete the item with specified key
            del item[key]
            self.count -= 1

            # check if we need to delete the table
            if len(item) == 0:
                self.table[pos] = None

            if len(item) == 1:
                # we need to move the item up
                for item in item.table:
                    if item is not None:
                        self.table[pos] = item
                        break
            return

        # Key is at current level
        if item[0] == key:
            self.table[pos] = None
            self.count -= 1
            return


    def __len__(self) -> int:
        """
        Returns the number of items in the hash table.
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        return ''
        result = ''
        for item in self.table:
            if item is not None:
                result += "↳ "
                result += item[0]

                if item[0][-1] == "*":
                    result += f"({len(item[1])})" # size of the table
                    result += "\n"
                    result += str(item[1])
                else:
                    result += f" = {item[1]}"
                    result += "\n"

        indented_result = ""
        for line in result.split("\n"):
            if line != "":
                indented_result += "|   " + line + "\n"

        return indented_result

    def get_location(self, key) -> list[int]:
        """
        Get the sequence of positions required to access this key.

        :raises KeyError: when the key doesn't exist.
        """

        pos = self.hash(key)
#         print(f"""
# ---------------------------------------------------------------------
# {key}
# {self.table}
# {position}
# ---------------------------------------------------------------------
#               """)

        if self.table[pos] is None:
            raise KeyError('Key does not exist')
        
        # 
        if isinstance(self.table[pos], InfiniteHashTable):
            return [pos] + self.table[pos].get_location(key)

        if self.table[pos][0] == key:
            return [pos]
        
        raise KeyError('Key does not exist')
    


    def __contains__(self, key: K) -> bool:
        """
        Checks to see if the given key is in the Hash Table

        :complexity: See linear probe.
        """
        try:
            _ = self[key]
        except KeyError:
            return False
        else:
            return True

    def sort_keys(self, current=None) -> list[str]:
        """
        Returns all keys currently in the table in lexicographically sorted order.
        """
        if current is None:
            current = []

        if self.table[self.TABLE_SIZE-1] is not None:
            current.append(self.table[self.TABLE_SIZE-1][0])

        for i in range(self.TABLE_SIZE):
            pos = (i-97)%self.TABLE_SIZE
            if pos == self.TABLE_SIZE-1:
                continue
            item = self.table[pos]
            if item is None:
                continue
            elif isinstance(item, InfiniteHashTable):
                item.sort_keys(current)
            else:
                current.append(item[0])

        return current
