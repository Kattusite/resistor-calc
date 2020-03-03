"""toolkit.py defines tools for determining which other resistors
can be built from a toolkit of primitive resistors.

For example, given a toolkit of resistors,
  * How close can we get to X ohms using no more than K resistors?
  * What is the smallest number of resistors we can use to reach X ohms exactly*?
  * What is the shallowest composite resistor we can build to reach X ohms exactly*?

A naive solution would be to exhaust the search space, by making all 2 resistor
combinations, then all three resistor combinations, then all 4 resistor combinations...

A better way might use heuristics to limit the number of paths that must be
explored, similar to beam search. If we want a 200KOhm resistor, we really don't
need to look at the 10, 20, 100 ohm resistors.
"""
import bisect
from collections import defaultdict

from resistor import Resistor

def withinTolerance(ohms, tol, resistor):
    """Returns True if resistor.ohms is in the range
    [ohms - tol*ohms, ohms + tol*ohms], else False."""
    actual = resistor.ohms
    delta = ohms * tol
    return ohms - delta <= actual and actual <= ohms + delta

class Toolkit:
    """Defines the primitive resistors available to our system.

    Fields:
      * resistors: a dictionary mapping from x to a sorted list of resistors
                   containing exactly x primitive resistors.
                   Note: Using a dict rather than a list lets us have a sparse
                   representation.
                   Note: Keeping the lists sorted by ohmage gives better opportunities
                   for efficiency
      * max_size: all composite resistors consisting of this many or fewer
                  primitive resistors are known to the Toolkit.
    """

    #########################################################################
    #                     Object overrides
    #########################################################################

    def __init__(self, rs):
        """Given rs, a list of the ohm values of the available resistances,
        create a Toolkit"""

        resistances = sorted(rs)
        self.resistors = defaultdict(lambda : [])
        self.resistors[1] = [Resistor(r) for r in resistances]
        self.max_size = 1

    def __contains__(self, resistor):
        if resistor.count not in self.resistors:
            return False

        # Binary search the list of resistors with resistor.count components
        a = self.resistors[resistor.count]
        i = bisect.bisect_left(a, resistor)

        # If a match was found, resistor is in this toolkit
        return i != len(a) and a[i] == resistor

    #########################################################################
    #                     Helpers
    #########################################################################

    def insert(self, resistor):
        """If the given resistor (or equivalent) is not already in the toolkit,
        add it to the appropriate list of resistors, in its proper sorted order.
        TODO: Decide whether equivalent resistors should count, or if they
        must be equal.
        """
        # Skip resistors already in the toolkit
        if resistor in self:
            return

        # Insert this resistor in sorted order
        # (WARNING: list inserts are slow, optimize later if needed)
        sz = resistor.count
        bisect.insort_left(self.resistors[sz], resistor)

    def find_le(self, k, ohms):
        """Return the rightmost resistor of exactly k primitives less than or
        equal to an equivalent resistance of ohms, or None if no such one exists.
        """
        if k not in self.resistors:
            return None
        x = Resistor(ohms)
        a = self.resistors[k]
        i = bisect.bisect_right(a,x)
        if i:
            return a[i-1]
        return None

    def find_ge(self, k, ohms):
        """Return the leftmost resistor of exactly k primitives greater than or
        equal to an equivalent resistance of ohms, or None if no such one exists.
        """
        if k not in self.resistors:
            return None
        x = Resistor(ohms)
        a = self.resistors[k]
        i = bisect.bisect_left(a,x)
        if i != len(a):
            return a[i]
        return None

    #########################################################################
    #                    Methods
    #########################################################################

    def brute_force(self, k=None):
        """Expand the toolkit's known resistors by building all composite resistors
        that contain no more than k primitive resistors.
        If k is not provided, use max_size+1
        (i.e. if we know all 2-large resistors, find all 3-large resistors)"""

        if k is None:
            k = self.max_size + 1

        # Note this loop shouldn't change the lists it is currently iterating
        # over, since it only affects self.resistors[i+1]
        for i in range(self.max_size, k):
            # Iterate over all i-sized resistors
            for r in self.resistors[i]:
                # Compose them with all 1-sized resistors
                for s in self.resistors[1]:
                    self.insert(r + s)
                    self.insert(r | s)

        self.max_size = k

    def closest(self, ohms, k=1, tolerance=0.1, n=1):
        """Return the k resistors we can build with less than n resistors,
        with an equivalent resistance closest to ohms. Exclude any results
        that are outside the tolerance (e.g. 0.1 ==> +/-10%)"""

        candidates = []

        # Iterate over all known buckets using <= k resistors
        cap = max(self.max_size, k) + 1
        for i in range(1, cap):
            # Find the closest resistors above and below.
            under = self.find_le(i, ohms)
            over  = self.find_ge(i, ohms)
            if over == under:
                over = None     # avoid duplicates

            if under and withinTolerance(ohms, tolerance, under):
                candidates.append(under)
            if over and withinTolerance(ohms, tolerance, over):
                candidates.append(over)

        candidates.sort(key=lambda r : abs(ohms - r.ohms))
        return candidates[:k]
