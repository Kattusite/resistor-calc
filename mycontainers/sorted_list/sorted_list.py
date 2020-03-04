from sortedcontainers import SortedList as LibSortedList

class SortedList(LibSortedList):
    """An actually good sorted list implementation, expanding the
    sortedcontainers type's API"""

    def append(self, item):
        return self.add(item)

    def find_ge(self, item):
        i = self.bisect_left(item)
        if i != len(self):
            return self[i]
        return None

    def find_le(self, item):
        i = self.bisect_right(item)
        if i:
            return self[i-1]
        return None
