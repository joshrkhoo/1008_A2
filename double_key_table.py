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
        if sizes is not None:
            self.sizes = sizes
        else:
            self.sizes = self.TABLE_SIZES

        # create the outer table first before checking the internal_sizes
        self.outer_table = LinearProbeTable(self.TABLE_SIZES) # LinearProbeTable has its own self.count
        self.outer_table.hash = lambda k: self.hash1(k) # set the outer table's hash function to hash1
        # will allow us to use the linear probing method in LinearProbeTable
        

        # table has been made so we can replace the existing TABLE_SIZES for the internal_sizes if necessary
        if internal_sizes is not None:
            self.internal_sizes = internal_sizes
        else:
            self.internal_sizes = self.TABLE_SIZES

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
        """
        # pos1 = self.hash1(key1)
        # pos2 = self.hash2(key2, self.TABLE_SIZES)

        # for _ in range(self.count):
        #     if self.table[pos1] is None:
        #         if is_insert:
        #             self.table[pos1] = LinearProbeTable(self.TABLE_SIZES)
        #             for _ in range(len(self.table[pos1])):
        #                 if self.table[pos1][pos2] is None:
        #                     return (pos1, pos2)
        #                 raise KeyError

        # ***NOTE***
        # because we are using LinearProbeTable to create the outer table, we can just use _linear_probe method 
        # for i in range(self.count): # only need to iterate over the cluster to find the next empty space
        #     if self.table[pos1] is None:
        #         if is_insert:
        #             # only create the inner table when pos1 hashes to None
        #             inner_table = LinearProbeTable(self.TABLE_SIZES) # self.TABLE_SIZES will be the internal_sizes input or sizes (if sizes is not None) or the original TABLE_SIZES (if both internal_sizes and sizes is None)
        #         else:
        #             raise KeyError # raise a KeyError 'when the key pair is not in the table, but is_insert is False'
                
        #         pos2 = self.hash2(key2, inner_table)
                
        #         for j in range(inner_table.count):
        #             inner_table._linear_probe(key2, is_insert)


        # use linear probing on the outer table to find the position of key1
        # the tuple at this postiion - (key1, inner table) - will have another hash table as the value of key1
        # use linear probing on the inner table to find the position of key2
        # the tuple at that position - (key2, value) - will be the actual value we want

        # if is_insert: # also want to check if the key is not in the table already
        #     inner_table = LinearProbeTable(self.internal_sizes)

        # pos1 = self.outer_table._linear_probe(key1, is_insert) # if is_insert is True, it will return the position in the outer hash table where we should create an inner table
        # self.outer_table[key1] = inner_table
        # pos2 = inner_table._linear_probe(key2, is_insert)


        # assume key1 is not in the table
        # get pos1 using linear probing for the self.outer_table
        # therefore self.outer_table[pos1] is None
        # we need to create a tuple (key1, inner_table) at self.outer_table[pos1]
        # then probe inner_table for pos2 (inner_table will be empty because we just created it)
        # return (pos1, pos2)

        # pos1 = self.outer_table._linear_probe(key1, is_insert)
        # # if key1 not in the outer table, create the inner table
        # inner_table = LinearProbeTable(self.internal_sizes)
        # inner_table.hash = lambda k: self.hash2(key2, inner_table)
        # # put this table at pos1
        # self.outer_table[key1] = inner_table
        # pos2 = inner_table._linear_probe(key2, is_insert)

        # assume key1 is in the table
        # get pos1
        # update the inner table at pos1 (key1, inner_table) - update inner_table


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
        if key1 in self.outer_table:
            pos1 = self.outer_table._linear_probe(key1, is_insert) # get its position if key1 is in the table
            inner_table = self.outer_table[key1]
        elif is_insert:
            inner_table = LinearProbeTable(self.internal_sizes) # create an inner table if key1 isn't in the table
            inner_table.hash = lambda k: self.hash2(key2, inner_table) # set the inner table's hash function
            self.outer_table[key1] = inner_table # using __setitem__ method from LPT
        else:
            raise KeyError

        pos2 = inner_table._linear_probe(key2, is_insert)
        return (pos1, pos2)



    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.
        """
        raise NotImplementedError()

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.
        """
        raise NotImplementedError()

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.
        """
        raise NotImplementedError()

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
        # key1, key2 = key # separate the keys

        # pos = self._linear_probe(key1, key2, False) # will be a tuple of positions

        # # if key1 doesn't exist, the KeyError will be raised by linear probe method from DKT
        # # if key1 exists but key2 doesn't exist, the KeyError will also be raised by linear prove method from DKT as a result of KeyError in the inner table

        # pos1, pos2 = pos

        # # go to pos1 in s

        # inner_table = self.outer_table[pos1][1] # don't think this actually works because self.outer_table is a LPT, not an array
        # data = inner_table[pos2][1]

        # return data
    
        # alternatively, could just use the methods in LPT such as __getitem__

        key1, key2 = key

        # KeyError will be raised by linear probe method in LPT if the key doesn't exist
        inner_table = self.outer_table[key1] # using __getitem__ from the LPT class
        value = inner_table[key2]

        return value

    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.
        """
        # separate the keys
        key1, key2 = key

        # check if the key is in the hash table
        # if key1 in self.outer_table: # using __contains__ from LPT
        #     # get the inner table
        #     inner_table = self.outer_table[key1] # looking for the inner table using __getitem__ from LPT
        #     inner_table[key2] = data

        # inner_table = LinearProbeTable(self.internal_sizes)
        # inner_table.hash = lambda k: self.hash2(k, inner_table)
        # self.outer_table[key1] = inner_table
        # inner_table[key2] = data

        increment_count = True # assume we are adding a new (key, value) pair

        if key1 in self.outer_table:
            inner_table = self.outer_table[key1]
            if key2 in inner_table: # if key2 is also in the table then we should not increment the count because we would be updating the data rather than adding new
                increment_count = False

        else:
            inner_table = LinearProbeTable(self.internal_sizes)
            inner_table.hash = lambda k: self.hash2(k, inner_table)
            self.outer_table[key1] = inner_table

        inner_table[key2] = data

        if increment_count:
            self.count += 1



        

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
        raise NotImplementedError()

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
        raise NotImplementedError()
