from __future__ import annotations

from typing import Generic, TypeVar, Iterator
from data_structures.hash_table import LinearProbeTable, FullError
from data_structures.referential_array import ArrayR

K1 = TypeVar('K1')
K2 = TypeVar('K2')
V = TypeVar('V')

class DoubleKeyTable(Generic[K1, K2, V]):
    """
    Double Hash Table.

    Type Arguments:
        - K1:   1st Key Type. In most cases should be string.
                Otherwise `hash1` should be overwritten.
        - K2:   2nd Key Type. In most cases should be string.
                Otherwise `hash2` should be overwritten.
        - V:    Value Type.

    Unless stated otherwise, all methods have O(1) complexity.
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        # if sizes is not None:
        #     self.sizes = sizes
        # else:
        #     self.sizes = self.TABLE_SIZES
        # if internal_sizes is not None:
        #     self.internal_sizes = internal_sizes
        # else:
        #     self.internal_sizes = self.TABLE_SIZES

        self.sizes = sizes or self.TABLE_SIZES
        self.internal_sizes = internal_sizes or self.TABLE_SIZES
        # self.size_index = 0
        # self.array:ArrayR[K1, LinearProbeTable[K2, V]] = ArrayR(self.sizes[self.size_index])
        self.count = 0

        self.outer_table: LinearProbeTable[K1, LinearProbeTable[K2, V]] = LinearProbeTable(self.sizes)
        self.outer_table.hash = lambda k: self.hash1(k)

    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
        # return self.outer_table.hash(key)

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % self.table_size
            a = a * self.HASH_BASE % (self.table_size - 1)
        return value

    def hash2(self, key: K2, sub_table: LinearProbeTable[K2, V]) -> int:
        """
        Hash the 2nd key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """
        # return sub_table.hash(key)

        value = 0
        a = 31415
        for char in key:
            value = (ord(char) + a * value) % sub_table.table_size
            a = a * self.HASH_BASE % (sub_table.table_size - 1)
        return value

    def _linear_probe(self, key1: K1, key2: K2, is_insert: bool) -> tuple[int, int]:
        """
        Find the correct position for this key in the hash table using linear probing.

        :raises KeyError: When the key pair is not in the table, but is_insert is False.
        :raises FullError: When a table is full and cannot be inserted.
        """
        if key1 not in self.outer_table:
            if is_insert:
                new_inner_table = LinearProbeTable(self.internal_sizes)
                new_inner_table.hash = lambda k: self.hash2(k, new_inner_table)
                self.outer_table[key1] = new_inner_table
            else:
                raise KeyError(key1)
        sub_table = self.outer_table[key1]
        return (
            self.outer_table._linear_probe(key1, False),
            sub_table._linear_probe(key2, is_insert)
        )




    #     # Position1 is the position of the top-level key
    #     position1 = self.hash1(key1)
    #     # print(position1)

    #     # sub_table is the bottom-level hash table for the top-level key   
    #     sub_table = self.array[position1]

    #     for _ in range(self.table_size):
    #         # No sub-table exists for the top-level key
    #         if sub_table is None:
    #             if is_insert:
    #                 # if is_insert is True and there is no, create a new sub-table
    #                 sub_table = LinearProbeTable(self.internal_sizes)
    #                 sub_table.hash = lambda k: self.hash2(k, sub_table)
    #             else:
    #                 raise KeyError
            

    

    #     # Position2 is the position of the bottom-level key
    #     position2 = self.hash2(key2, sub_table)
    #     # print(position2)
    #     # Linear probe through the bottom-level hash table
    #     for _ in range(sub_table.table_size):
    #         if sub_table.array[position2] is None:
    #             # Empty spot. Am I upserting or retrieving?
    #             if is_insert:
    #                 return (position1, position2)
    #             else:
    #                 raise KeyError(key2)
    #         elif sub_table.array[position2][0] == key2:
    #             return (position1, position2)
    #         else:
    #             # Taken by something else. Time to linear probe.
    #             position2 = (position2 + 1) % sub_table.table_size

        
        

    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        if key:
            return self.outer_table[key].keys()
        return self.outer_table.keys()


        # if key is None:
        #     return [k1 for k1 in self.iter_keys()]
        # else:
        #     # Position1 is the position of the top-level key
        #     position1 = self.hash1(key)
        #     # sub_table is the bottom-level hash table for the top-level key
        #     sub_table = self.array[position1]
        #     # Iterate through the bottom-level hash table and return all keys
        #     if sub_table is not None:
        #         return [k2 for k2 in sub_table.iter_keys()]
        #     else:
        #         return [] 




    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        :raises KeyError: When the key is not in the table.
        """
        # If key is None, iterate through all top-level keys
        if key is None:
            for tup in self.outer_table.array:
                if tup is not None:
                    yield tup[0]


        # Else, iterate through all bottom-level keys for top-level key k
        else:
            if key not in self.outer_table:
                raise KeyError(key)

            sub_table = self.outer_table[key]

            for tup in sub_table.array:
                if tup is not None:
                    yield tup[0]

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        # If key is None, iterate through all top-level keys
        if key is None:
            for outer_tup in self.outer_table.array:
                if outer_tup is not None:
                    for inner_tup in outer_tup[1].array:
                        if inner_tup is not None:
                            yield inner_tup[1]


        # Else, iterate through all bottom-level keys for top-level key k
        else:
            if key not in self.outer_table:
                raise KeyError(key)

            sub_table = self.outer_table[key]

            for tup in sub_table.array:
                if tup is not None:
                    yield tup[1]

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        if key:
            return self.outer_table[key].values()
        
        values = []
        for sub_table in self.outer_table.values():
            values.extend(sub_table.values())
        return values

        # if key is None:
        #     return [v for v in self.iter_values()]
        # else:
        #     position1 = self.hash1(key)
        #     sub_table = self.outer_table[position1]
        #     if sub_table is not None:
        #         return [v for v in sub_table.iter_values()]
        #     else:
        #         return []


    def __contains__(self, key: tuple[K1, K2]) -> bool:
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

    def __getitem__(self, key: tuple[K1, K2]) -> V:
        """
        Get the value at a certain key

        :raises KeyError: when the key doesn't exist.
        """
        k1, k2 = key

        # KeyError is raised by the LinearProbeTable class
        sub_table = self.outer_table[k1]
        return sub_table[k2]

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :raises FullError: when the table cannot be resized further.
        """
        k1, k2 = key

        if k1 not in self.outer_table:
            self.outer_table[k1] = LinearProbeTable(self.internal_sizes)
            self.outer_table[k1].hash = lambda k: self.hash2(k, self.outer_table[k1])

        sub_table = self.outer_table[k1]
        sub_table[k2] = data

        self.count += 1
        

        # self.count += 1


        # # Get the position of the key - tuple of 2 ints
        # position = self._linear_probe(key[0], key[1], True)
        
        # if self.array[position[0]] is None:
        #     self.count += 1
        # self.array[position[0]] = key[0]
        # self.array[position[0]][position[1]] = (key[1], data)

        # # Resize if necessary
        # if len(self) > self.table_size / 2:
        #     self._rehash()
        
    


    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        k1, k2 = key
        del self.outer_table[k1][k2]
        if len(self.outer_table[k1]) == 0:
            del self.outer_table[k1]
        self.count -= 1

    # def _rehash(self) -> None:
    #     """
    #     Need to resize table and reinsert all values

    #     :complexity best: O(N*hash(K)) No probing.
    #     :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
    #     Where N is len(self)
    #     """
    #     self.outer_table._rehash()
    #     # Create a new array with the next size
    #     self.size_index += 1
    #     new_array = ArrayR(self.TABLE_SIZES[self.size_index])

    #     # Iterate through the old array and rehash all values
    #     for sub_table in self.array:
    #         if sub_table is not None:
    #             for k2 in sub_table:
    #                 pos = self._linear_probe(sub_table[k2], k2, True)
    #                 new_array[pos[0]][pos[1]] = sub_table[k2]

    #     # Assign the new array to the old array
    #     self.array = new_array

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        # return self.sizes[self.size_index]
        return self.outer_table.table_size

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        # return str(self.outer_table)

        result = ""
        for i, val in enumerate(self.outer_table.array):
            if val is None:
                result += f"{i}, None\n"
                continue
            result += f"{i}, {val[0]}, {val[1]}\n"
        return result
