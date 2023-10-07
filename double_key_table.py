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


        self.sizes = sizes or self.TABLE_SIZES
        self.internal_sizes = internal_sizes or self.TABLE_SIZES

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

        :complexity best: O(hash(key1) + hash(key2)) 
            - Occurs when hash position is empty
        :complexity worst: O(hash(key1) + N*comp(K1) + hash(key2) + M*comp(K2)) 
            - Occurs when we have to search the entire table
            - N is the size of the outer table, M is the size of the inner table
        """

        # If statement checks if outer table has key1 and if it doesnt then we either add it or raise a key error
        if key1 not in self.outer_table:
            if is_insert:
                # if is_insert is True and there is no inner table for key1, create a new inner table
                new_inner_table = LinearProbeTable(self.internal_sizes)
                # set the hash function of the new inner table to be the hash2 function
                new_inner_table.hash = lambda k: self.hash2(k, new_inner_table)
                # insert the new inner table into the outer table at key1
                    # essentially, key 1 and the new inner table get inserted into the outer table
                    # key1 just points to the new inner table
                self.outer_table[key1] = new_inner_table
            else:
                raise KeyError(key1)
        
        # get the inner table for key1
        sub_table = self.outer_table[key1]

        # return the position of key1 and key2
            # Uses the linear probe function implemented in the LinearProbeTable class
        return (
            self.outer_table._linear_probe(key1, False),
            sub_table._linear_probe(key2, is_insert)
        )
            
    def keys(self, key:K1|None=None) -> list[K1|K2]:
        """
        key = None: returns all top-level keys in the table.
        key = x: returns all bottom-level keys for top-level key x.

        :complexity: 
        Best case: O(N) where N is the number of keys in the outter table.
            - Occurs when there is no key given and we have to iterate through the outer table.

        Worse case: O(hash(key) + M) where M is the number of keys in the inner table.
            - Occurs when there is a key given and the key is in the outer table.

        """

        if key:
            # keys() gets all the keys in the hash table
                # here we get all the keys at the inner hash table which is pointed to by key
            return self.outer_table[key].keys()
        # if key is None, return all the keys in the outer hash table
        return self.outer_table.keys()


    def iter_keys(self, key:K1|None=None) -> Iterator[K1|K2]:
        """
        key = None:
            Returns an iterator of all top-level keys in hash table
        key = k:
            Returns an iterator of all keys in the bottom-hash-table for k.

        :raises KeyError: When the key is not in the table.

        :complexity: 
        Best case: O(N)
            - N is the number of keys in the outer table.

        Worst case: O(hash(key)) + M
            - M is the number of keys in the inner table

        """
        # If key is None, iterate through all top-level keys
        if key is None:
            # Iterate through all top-level keys
            # use array attribute of outer table to iterate through all the keys
            for tup in self.outer_table.array:
                # if the key is not None, yield the key
                # yield is like return but it returns a generator
                if tup is not None:
                    yield tup[0]


        # Else, iterate through all bottom-level keys for top-level key k
        else:
            # if key is not in the outer table, raise a key error
            if key not in self.outer_table:
                raise KeyError(key)

            # get the inner table for key
            sub_table = self.outer_table[key]

            # iterate through the inner table
            for tup in sub_table.array:
                if tup is not None:
                    # tup[0] is the key tup[1] is the value
                    yield tup[0]

    def iter_values(self, key:K1|None=None) -> Iterator[V]:
        """
        key = None:
            Returns an iterator of all values in hash table
        key = k:
            Returns an iterator of all values in the bottom-hash-table for k.

        :complexity:
        Best case: O(hash(key) + M)
            - M is the number of keys in the inner table.
            - Occurs when there is a key given and the key is in the outer table.
        
        Worst case: O(N*M)
            - N is the number of keys in the outer table.
            - M is the number of keys in the inner table.
            - Occurs when there is no key given and we have to iterate through inner and outter table.
        """
        # Get all values in all inner tables
        # If key is None, iterate through all top-level keys
        if key is None:
            # Iterate through outter table
            for outer_tup in self.outer_table.array:
                if outer_tup is not None:
                    # Iterate through inner table
                    # outer_tup[1] is the inner table
                    for inner_tup in outer_tup[1].array:
                        if inner_tup is not None:
                            yield inner_tup[1]


        # Get all values in the single inner table pointed to by key
        # Else, iterate through the bottom hash table pointed to by key
        else:
            # if key is not in the outer table, raise a key error
            if key not in self.outer_table:
                raise KeyError(key)

            # get the inner table for key
            sub_table = self.outer_table[key]

            # iterate through the inner table
            for tup in sub_table.array:
                if tup is not None:
                    yield tup[1]

    def values(self, key:K1|None=None) -> list[V]:
        """
        key = None: returns all values in the table.
        key = x: returns all values for top-level key x.

        :complexity: 
        Best case = O(hash(key) + N) 
            - N is the number of keys in the table.
            - Occurs when there is a key given


        Worst case = O(N*M) 
            - N is the number of keys in the inner table
            - M is the number of keys in the outter table
            - Occurs when there is no key given and we have to iterate through the outer table

        """

        # Get all values at the inner table pointed to by key
        if key:
            return self.outer_table[key].values()
        
        # Get all values in all inner tables
        values = []
        # Iterate through the outer table
        for sub_table in self.outer_table.values():
            # add all values in the inner table to the values list
            values.extend(sub_table.values())
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

        :complexity: See linear probe.

        """

        # K1 = key[0], K2 = key[1]
        k1, k2 = key

        # KeyError is raised by the LinearProbeTable class
        sub_table = self.outer_table[k1]
        return sub_table[k2]
    


    def __setitem__(self, key: tuple[K1, K2], data: V) -> None:
        """
        Set an (key, value) pair in our hash table.

        :raises FullError: when the table cannot be resized further.

        :complexity: see linear probe.

        """

        k1, k2 = key

        # If key1 is not in the outer table, create a new inner table for key1
        if k1 not in self.outer_table:
            self.outer_table[k1] = LinearProbeTable(self.internal_sizes)
            self.outer_table[k1].hash = lambda k: self.hash2(k, self.outer_table[k1])

        # Get the inner table for key1
        sub_table = self.outer_table[k1]
        # assign the value to the inner table at key2
        sub_table[k2] = data

        # Increment count of the outer table
        self.count += 1
        

    def __delitem__(self, key: tuple[K1, K2]) -> None:
        """
        Deletes a (key, value) pair in our hash table.

        :raises KeyError: when the key doesn't exist.

        :complexity: See linear probe.
        """

        k1, k2 = key
        # Delete the value from the inner table at key2
        del self.outer_table[k1][k2]
        # If the inner table is empty, delete the inner table from the outer table
        if len(self.outer_table[k1]) == 0:
            del self.outer_table[k1]

        # decrement count of the outer table
        self.count -= 1

    def _rehash(self) -> None:
        """
        Need to resize table and reinsert all values

        :complexity: See LinearProbeTable implementation

        This function is not implemented as DoubleKeyTable uses the LinearProbeTable implementation.
        """
        pass

    @property
    def table_size(self) -> int:
        """
        Return the current size of the table (different from the length)

        :complexity: O(1)
        """

        return self.outer_table.table_size

    def __len__(self) -> int:
        """
        Returns number of elements in the hash table

        :complexity: O(1)
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
