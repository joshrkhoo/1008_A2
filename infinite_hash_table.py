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

        Complexity:
            Best case = O(1)
                - item is not a sub table
            Worst case = O(l)
                - l is the length of the key
                - This is because we need to recursively call the function l times
        """
        
        pos = self.hash(key)

        item = self.table[pos]

        if item is None:
            raise KeyError('Key does not exist')

        # Get the value from the sub table
            # item can be a sub table
            # this is a recursive call
        if isinstance(item, InfiniteHashTable):
            return item[key]

        if item[0] == key:
            return item[1]


    def __setitem__(self, key: K, value: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        Complexity:
            Best case = O(1)
                - No conflicts
            Worst case = O(l)
                - l is the length of the key
                - This is because we need to recursively call the function l times 
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

        Complexity: 
            Best case = O(1)
                - item is not a sub table
            Worst case = O(l)
                - l is the length of the key
                    - This is because we may need to recursively call the function l times to get the key

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

            # Instead of having an infinitehashtable instance, we can just have the key and value
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

        Complexity: Best/Worst case = O(1)
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

        Complexity: Best/Worst case = O(n)
            - n is the length of the key
            - This is because we need to recursively call the function n times
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
        
        # Recursively call the function if we have a sub table
            # This is done to get the sequence of positions required to access this key
        if isinstance(self.table[pos], InfiniteHashTable):
            # adds the current position and list of positions from the recursive call together
                # then returns the list when the recursive call is finished
            return [pos] + self.table[pos].get_location(key)

        # No sub table, only the key, return the position
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
            
        Simplified Complexity:
            Best Case = O(1)
                - No sub table to traverse
                - For loop is constant O(1) due to the table size being constant
            Worst case = O(N)
                - N is the number of keys in the table
                    - The for loop is constant O(1) due to the table size being constant
                    - Recursively calling the function is O(N) due to the number of keys in the table
                    - All other operations are constant O(1)

        """


        if current is None:
            current = []

        # Add the last item in the table
            # This will only occur when the conflicts keep occuring until one of the keys length is less than the current level
                # Looking at lin and linked, when the level is 3, the key lin will be in the last slot of the table
        if self.table[self.TABLE_SIZE-1] is not None:
            current.append(self.table[self.TABLE_SIZE-1][0])

        # Iterate though each slot in the table
        for i in range(self.TABLE_SIZE):

            # Eseentially mapping indexes to lower case letters 'a' to 'z' 
                # And finding the position in the table by using modulo
            pos = (i+97)%self.TABLE_SIZE

            # Skip the last item in the table
            if pos == self.TABLE_SIZE-1:
                continue

            # Get the item at pos
            item = self.table[pos]

            # Skip if no item
            if item is None:
                continue
            
            # If the item is a sub table, recursively call the function
                # This is done to get the keys in the sub table
            elif isinstance(item, InfiniteHashTable):
                item.sort_keys(current)
            # Otherwise, add the key to the list
            else:
                current.append(item[0])

        return current
