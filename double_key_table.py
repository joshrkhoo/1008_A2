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

    Complexity:
    Best case = Worst case = O(n) where n is the size of the outer table. Occurs because we create an array of size n for the table
    """

    # No test case should exceed 1 million entries.
    TABLE_SIZES = [5, 13, 29, 53, 97, 193, 389, 769, 1543, 3079, 6151, 12289, 24593, 49157, 98317, 196613, 393241, 786433, 1572869]

    HASH_BASE = 31

    def __init__(self, sizes:list|None=None, internal_sizes:list|None=None) -> None:
        if sizes is not None: # O(1)
            self.sizes = sizes # O(1)
        else:
            self.sizes = self.TABLE_SIZES # O(1)

        if internal_sizes is not None: # O(1)
            self.internal_sizes = internal_sizes # O(1)
        else:
            self.internal_sizes = self.TABLE_SIZES # O(1)

        self.outer_table = LinearProbeTable(self.sizes) # O(n) where n is the table size
        # LinearProbeTable has its own self.count
        self.outer_table.hash = lambda k: self.hash1(k) # O(1)
        # set the outer table's hash function to hash1
        # will allow us to use the linear probing method in LinearProbeTable
        
        self.count = 0 # count for the double key table (should count all the values in all tables (top and bottom))


    def hash1(self, key: K1) -> int:
        """
        Hash the 1st key for insert/retrieve/update into the hashtable.

        :complexity: O(len(key))
        """

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

        Complexity:
        Best case is O(hash(key1) + hash(key2)). Occurs when the position of key1 in the outer table is its hashed value and an inner table is already paired with key1.
        Additionally, we locate key2 at its hashed position
        Worst case is O(hash(key1) + n + hash(key2))
        """
        # check if key1 is in the table
        # if key1 in self.outer_table:
        #     pos1 = self.outer_table._linear_probe(key1, is_insert)
        #     pos2 = inner_table._linear_probe(key2, is_insert)
        #     return (pos1, pos2)
        
        # if is_insert:
        #     inner_table = LinearProbeTable(self.internal_sizes)
        #     inner_table.hash = lambda k: self.hash2(key2, inner_table)
        #     self.outer_table[key1] = inner_table
        #     pos1 = self.outer_table._linear_probe(key1, is_insert)
        #     pos2 = inner_table._linear_probe(key2, is_insert)
        #     return (pos1, pos2)

        # raise KeyError
        # if key1 is in the table, then we already have an inner table

        # check if key1 is in the outer table using the __contains__ method from LPT
        if key1 in self.outer_table: # O(__contains__)
            # pos1 = self.outer_table._linear_probe(key1, is_insert) # get its position if key1 is in the table
            # commented out pos1 above because otherwise it is possible for pos1 to be undefined when we try to return
            # if key1 isn't in the table, we can just look for the available position anyway - doesn't need to be in this 'if' statement
            inner_table = self.outer_table[key1] # O(__getitem__)
        elif is_insert:
            inner_table = LinearProbeTable(self.internal_sizes) # O(n) where n is the table size
            # create an inner table if key1 isn't in the table
            inner_table.hash = lambda k: self.hash2(key2, inner_table) # O(1)
            # set the inner table's hash function
            self.outer_table[key1] = inner_table # O(__setitem__)
            # using __setitem__ method from LPT
        else:
            raise KeyError

        pos1 = self.outer_table._linear_probe(key1, is_insert)
        pos2 = inner_table._linear_probe(key2, is_insert)
        return (pos1, pos2)



    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        Complexity:
        Best case is O(n) where n is the number of elements in the top table. Occurs when the key is None
        Worst case is O(hash(key) + m) where m is the number of elements in the bottom table. Occurs when there is a key
        """

        if key is None:
            table = self.outer_table
        else:
            table = self.outer_table[key]

        for item in table.array:
            if item is not None:
                yield item[0]

        # if key is None:
        #     for item in self.outer_table:
        #         if item is not None:
        #             yield item[0]
        # else:
        #     inner_table = self.outer_table[key]
        #     for item in inner_table:
        #         if item is not None:
        #             yield item[0]

    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        Complexity:
        Best case is O(n) where n is the number of elements in the top table. Occurs when the key is None
        Worst case is O(hash(key) + m) where m is the number of elements in the bottom table. Occurs when there is a key
        """
        # return list(self.iter_keys(key))

        key_iterator = self.iter_keys(key) 

        keys = []
        for key in key_iterator: # we can iterate over our iterator
            keys.append(key)

        return keys

            

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        Complexity:
        Best case is O(hash(key) + n) where n is the number of elements in the outer table
        Occurs when there is a key
        Worst case is O(n*m) where n is the number of elements in the outer table and m
        is the number of elements in the lower table
        Occurs when there is no key
        """
        
        if key is None:
            table = self.outer_table
        else:
            table = self.outer_table[key]

        if key is None:
            for outer_item in table.array:
                if outer_item is not None:
                    inner_table = outer_item[1]
                    for inner_item in inner_table.array:
                        if inner_item is not None:
                            yield inner_item[1]
        else:
            for item in table.array:
                if item is not None:
                    yield item[1]

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        Complexity:
        Best case is O(hash(key) + n + k) where n is the number of elements in the outer table
        and k is the number of elements in the generator
        Occurs when there is no key
        Worst case is O(n*m) where n is the number of elements in the outer table, m
        is the number of elements in the lower table
        Occurs when there is a key
        """
        values = []
        value_iterator = self.iter_values(key)

        for value in value_iterator: # we can iterate over our iterator
            values.append(value)

        return values

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
        key1, key2 = key # O(1)

        # KeyError will be raised by linear probe method in LPT if the key doesn't exist
        inner_table = self.outer_table[key1] # using __getitem__ from the LPT class
        value = inner_table[key2]

        return value

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        # implementation 1 - using methods from LPT
        # separate the keys
        key1, key2 = key
        increment_count = True # assume we are adding a new (key, value) pair

        # check if the key is in the hash table
        if key1 in self.outer_table: # using __contains__ from LPT
            inner_table = self.outer_table[key1] # looking for the inner table using __getitem__ from LPT
            if key2 in inner_table: # if key2 is also in the table then we should not increment the count because we would be updating the data rather than adding new
                increment_count = False

        else:
            inner_table = LinearProbeTable(self.internal_sizes)
            inner_table.hash = lambda k: self.hash2(k, inner_table)
            self.outer_table[key1] = inner_table

        inner_table[key2] = data

        if increment_count:
            self.count += 1

    
        # # implementation 2 - accessing the array of the LPTs (unsure)
        # # separate the keys
        # key1, key2 = key
        # pos = self._linear_probe(key1, key2, True) # will create an inner table if key1 is not in the table
        # pos1, pos2 = pos

        # if self.outer_table.array[pos1] is None:
        #     self.count += 1 # increment count of DKT
        #     self.outer_table.count += 1 # increment count of LPT

        # # inner_table = self.outer_table[key1]
        # inner_table = self.outer_table.array[pos1][1]

        # if inner_table.array[pos2] is None:
        #     self.count += 1
        #     inner_table.count += 1

        # # inner_table[key2] = data
        # inner_table.array[pos2] = (key2, data)

        # # self.outer_table[key1] = inner_table
        # self.outer_table.array[pos1] = (key1, inner_table)






        

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.
        """
        key1, key2 = key

        # if key1 in self.outer_table:
        #     inner_table = self.outer_table[key1]
        #     if key2 in inner_table:
        #         del inner_table[key2]
    
        #     if len(inner_table) == 0:
        #         del self.outer_table[key1]

        # linear probe method from LPT will raise the KeyErrors 
        inner_table = self.outer_table[key1]
        del inner_table[key2]

        if len(inner_table) == 0:
            del self.outer_table[key1]

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity best: O(N*hash(K)) No probing.
        :complexity worst: O(N*hash(K) + N^2*comp(K)) Lots of probing.
        Where N is len(self)
        """
        pass

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)
        """
        return self.outer_table.table_size

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table
        """

        # should return the total number of items across all sub-tables
        # so return the number of values in the outer table + the number of values in the inner table        
    
        return self.count

    def __str__(self) -> str:
        """
        String representation.

        Not required but may be a good testing tool.
        """
        result = ""
        for i, val in enumerate(self.outer_table.array):
            if val is None:
                result += f"{i}, None\n"
                continue
            result += f"{i}, {val[0]}, {val[1]}\n"
        return result
