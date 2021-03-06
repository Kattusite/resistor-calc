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

# TODO: Implement some fun dynamic programming-ish solution
# or some heuristic to more efficiently get close to a target resistance

# TODO: An alternative problem formulation:
#   In the common use case, we don't actually care about *all resistors possible*
#   using a given toolkit. Most resistors are +/- 1% tol anyway, and most
#   are specified using just 3 significant digits (i.e. in color bands)
#   So we can "uniquely" define resistors by their color codes.
#   It is easy to enumerate all possible color codes (12 colors ^ 4 meaningful bands)
#   So we can have a table mapping from 4 digit base-12 color codes
#   to implementations.
#
#   e.g. 9043 => 904k Ohms
#        4720 => 472  Ohms
#
#   For each of these bins, we don't need to track *every possible* implementation,
#   only "interesting" ones: (least resistors, least depth, least breadth)
#
#   This gives us a max. storage of:
#     wrong: (12 color bases ** 4 digits) * 3 interesting ~= 60_000 < 2^16
#   : actually it's (10*10*10*12) * 3 == 36000
#     Not that bad!
#   We could theoretically just try to fill in the entire table, and ignore
#   other implementations.
#   Worth thinking about this idea more:
#     * Does it improve upon the brute force / pruned brute force approaches? How?
#     * What are the different use cases for the two approaches?
#     * Does either implementation allow a richer API?
#     * How would end-users want to use Toolkit? What functions would they call?
#     * Can it be used as a more informed pruning strategy, by rejecting new
#       insertions when that resistor's bin is already occupied by a more
#       'interesting' resistor
#

from collections import defaultdict

from resistor import Resistor
from mycontainers import SortedList # a wrapper for sortedcontainers.SortedList

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

    def __init__(self, rs, Container=SortedList):
        """Given rs, a list of the ohm values of the available resistances,
        create a Toolkit"""

        resistances = sorted(rs)
        self.resistors = defaultdict(Container)
        for r in resistances:
            self.resistors[0].add(Resistor(r))
            self.resistors[1].add(Resistor(r))
        self.max_size = 1

    def __contains__(self, resistor):
        n = resistor.numPrimitives()
        if n not in self.resistors:
            return False
        return resistor in self.resistors[n]

    def fuzzy_contains(self, resistor, tol=0.01):
        """Return true if self.resistors contains a resistor within a tol*ohms
        sized window around the given resistance."""
        tgt = resistor.ohms
        for n, a in self.resistors.items():
            above = a.find_ge(resistor)
            if above and withinTolerance(resistor.ohms, tol, above):
                return True

            # TODO: Is it necessary to check both above and below or just one?
            below = a.find_le(resistor)
            if below and withinTolerance(resistor.ohms, tol, below):
                return True

        return False

    #########################################################################
    #                     Helpers
    #########################################################################

    def insert(self, resistor, tol=0):
        """If the given resistor (or equivalent) is not already in the toolkit,
        add it to the appropriate list of resistors, in its proper sorted order.
        TODO: Decide whether equivalent resistors should count, or if they
        must be equal.
        """
        # Skip resistors already in the toolkit
        if not tol and resistor in self:
            return
        elif tol and self.fuzzy_contains(resistor, tol=tol):
            return

        # Insert this resistor in sorted order
        n = resistor.numPrimitives()
        # self.resistors[0].add(resistor) # allows richer queries, but ~doubles runtime
        self.resistors[n].add(resistor)

    #########################################################################
    #                    Methods
    #########################################################################

    def brute_force(self, k=None, pruneTolerance=0):
        """Expand the toolkit's known resistors by building all composite resistors
        that contain no more than k primitive resistors.
        If k is not provided, use max_size+1
        (i.e. if we know all 2-large resistors, find all 3-large resistors).

        If prune is provided, do not add a new resistor to the inventory if its
        equivalent resistance is within prune proportion of the next closest resistor.
        (i.e. if 0.01, don't add resistors within 1% of a known resistor)
        """

        if k is None:
            k = self.max_size + 1

        # Note this loop shouldn't change the lists it is currently iterating
        # over, since it only affects self.resistors[i+1]
        for i in range(self.max_size, k):
            # Iterate over all i-sized resistors
            for r in self.resistors[i]:
                # Compose them with all 1-sized resistors
                for s in self.resistors[1]:
                    self.insert(r + s, tol=pruneTolerance)
                    self.insert(r | s, tol=pruneTolerance)

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
            rs = self.resistors[i]
            r = Resistor(ohms)
            under = rs.find_le(r)
            over  = rs.find_ge(r)
            if over == under:
                over = None     # avoid duplicates

            if under and withinTolerance(ohms, tolerance, under):
                candidates.append(under)
            if over and withinTolerance(ohms, tolerance, over):
                candidates.append(over)

        candidates.sort(key=lambda r : abs(ohms - r.ohms))
        return candidates[:k]

    def biggestGap(self, k):
        """Return the resistance of the resistor that is least-buildable
        using k resistors of this toolkit.

        More concretely, compute ratio = r[i] / r[i-1] for all i,
        and return the value halfway between r[i], r[i-1] for the largest
        such ratio"""
        if k not in self.resistors:
            raise ValueError
        rs = self.resistors[k]
        ratios = [ rs[i].ohms / rs[i-1].ohms for i in range(1, len(rs)) ]

        topRatio, topIndex = -1, -1
        for i, ratio in enumerate(ratios):
            if ratio > topRatio:
                topRatio, topIndex = ratio, i

        above, below = rs[topIndex+1], rs[topIndex]
        mid = Resistor((above.ohms + below.ohms) / 2)

        return (below, mid, above)

    def displayInventory(self, n=3):
        print("====== Resistor inventory ======")
        for i in range(1, self.max_size+1):
            rs = self.resistors[i]
            print(f"------ {i}x Resistor ({len(rs)} known) ------")
            if n == 0:
                continue
            for j, r in enumerate(rs):
                print(repr(r))
                if j > n:
                    print("...")
                    break
