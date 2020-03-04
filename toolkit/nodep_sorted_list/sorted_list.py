import bisect
from collections.abc import MutableSequence

class SortedList(MutableSequence):
    """A sorted list operation using a builtin list and the bisect
    library operations.

    Basically a (much) less efficient version of sorted_list that doesn't
    require any dependencies"""

    def __init__(self):
        self.a = []

    def __len__(self):
        return len(self.a)

    def __iter__(self):
        return self.a.__iter__()

    def __str__(self):
        return self.a.__str__()

    def __repr__(self):
        return self.a.__repr__()

    def index(self, item):
        i = bisect.bisect_left(self.a,item)
        if i != len(self.a) and self.a == item:
            return i
        raise ValueError

    def find_lt(self, item):
        i = bisect.bisect_left(self.a, item)
        if i:
            return self.a[i-1]
        return None

    def find_le(self, item):
        i = bisect.bisect_right(self.a, item)
        if i:
            return self.a[i-1]
        return None

    def find_gt(self, item):
        i = bisect.bisect_right(self.a, item)
        if i != len(self.a):
            return self.a[i]
        return None

    def find_ge(self, item):
        i = bisect.bisect_left(self.a, item)
        if i != len(self.a):
            return self.a[i]
        return None

    def __contains__(self, item):
        i = bisect.bisect_left(self.a,item)
        return i != self.size and self.a[i] == item

    def __getitem__(self, key):
        return self.a[key]

    def __delitem__(self, key):
        """Could be implemented, but we dont need it for this use case"""
        return NotImplemented

    def __setitem__(self, key, value):
        """Users should not explicitly set values at a given index, as this
        could lead to violation of the sorting invariant"""
        return NotImplemented

    def insert(self, key, value):
        """Users should not explicitly set values at a given index, as this
        could lead to violation of the sorting invariant"""
        return NotImplemented

    def append(self, value):
        bisect.insort_left(self.a, value)

    def add(self,value):
        return self.append(value)
