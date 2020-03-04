import bisect
from collections.abc import MutableSequence

def newArray(capacity):
    return [None for i in range(capacity)]

class SortedArray(MutableSequence):
    """A data structure that represents a sorted array of elements.

    The array resizes in batches for amortized constant time insertion."""

    def __init__(self, capacity=16):
        self.size = 0
        self.capacity = capacity

        self.a = newArray(capacity)

    def __len__(self):
        return self.size

    def __iter__(self):
        return self.a[:len(self)].__iter__()

    def __str__(self):
        return f"[{', '.join([str(x) for x in self])}]"

    def __repr__(self):
        return f"[{', '.join([repr(x) for x in self])}]"

    def index(self, item):
        i = bisect.bisect_left(self.a,item,hi=self.size)
        if i != len(self.a) and self.a == item:
            return i
        raise ValueError

    def find_lt(self, item):
        i = bisect.bisect_left(self.a, item, hi=self.size)
        if i:
            return self.a[i-1]
        return None

    def find_le(self, item):
        i = bisect.bisect_right(self.a, item, hi=self.size)
        if i:
            return self.a[i-1]
        return None

    def find_gt(self, item):
        i = bisect.bisect_right(self.a, item, hi=self.size)
        if i != len(self.a):
            return self.a[i]
        return None

    def find_ge(self, item):
        i = bisect.bisect_left(self.a, item, hi=self.size)
        if i != len(self.a):
            return self.a[i]
        return None

    def __contains__(self, item):
        i = bisect.bisect_left(self.a,item,hi=self.size)
        return i != self.size and self.a[i] == item

    def __getitem__(self, key):
        if key < 0 or key >= self.size:
            raise IndexError("list index out of range")
        return self.a[key]

    def __delitem__(self, key):
        """Could in principle be implemented, but not necessary for the
        resistors use case"""
        return NotImplemented

    def __setitem__(self, key, value):
        """Users should not explicitly set values at a given index, as this
        could lead to violation of the sorting invariant"""
        return NotImplemented

    def insert(self, key, value):
        """Users should not explicitly set values at a given index, as this
        could lead to violation of the sorting invariant"""
        return NotImplemented

    def resize(self, capacity):
        a = newArray(capacity)
        for i in range(self.size):
            a[i] = self.a[i]
        self.a = a
        self.capacity = capacity

    def expand(self):
        self.resize(self.capacity * 2)

    def shrink(self):
        self.resize(self.capacity // 2)

    def append(self, value):
        if self.size == self.capacity:
            self.expand()

        # One iteration of insertion sort
        self.a[self.size] = value
        for i in range(self.size, -1, -1):
            if i > 0 and self.a[i] < self.a[i-1]:
                self.a[i], self.a[i-1] = self.a[i-1], self.a[i]
            else:
                break

        self.size += 1

    def add(self,value):
        return self.append(value)
