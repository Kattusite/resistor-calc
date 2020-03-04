"""resistor.py defines the Resistor class, which defines a collection of useful
ways to compose and work with electrical resistors.

Terminology:
  * A "primitive" resistor is one consisting of just a single physical component
  * A "composite" or "complex" resistor consists of several smaller components,
    primitive or composite, arranged in series and/or parallel.

TODO:
  * Resistor color code handling / representation
"""

from .schematic import Schematic
from .const import SERIES, PARALLEL

class Resistor():
    """Resistor represents a resistor (either  a primitive or composite of primitives).

    Fields:
        * ohms: how many (equivalent) ohms of resistance the resistor has
        * tolerance: the tolerance, in percentage points (i.e. 1 == 1% == 0.01)
        * count: how many primitive resistors the resistor has
        * depth: the number of resistors on the longest path
        * history: a dictionary, or None for primitive resistors
            * parents: a (Resistor,Resistor) tuple of this resistor's ancestors
            * operation: indicates how parents combine to form this resistor
                (SERIES or PARALLEL)

    WARNING: Tolerance propagation is not yet supported!
        * We naively set tolerance to the max of all components, but
          this is probably incorrect.
    """

    ########################################################################
    #                         Object overrides
    ########################################################################

    def __init__(self, ohms, tolerance=1, count=1, depth=1):
        if ohms < 0:
            raise ValueError(f"ohms cannot be negative! ({ohms} < 0)")
        if tolerance < 0:
            raise ValueError(f"tolerance cannot be negative! ({ohms} < 0)")
        if count <= 0:
            raise ValueError(f"number of resistors must be positive! ({count} <= 0)")
        if depth <= 0:
            raise ValueError(f"longest path must have positive length! ({depth} <= 0)")

        self.ohms = ohms
        self.tolerance = tolerance
        self.count = count
        self.depth = depth

        self.history = None

    def merge(self, other, op):
        """A helper function for series/parallel. This helper does all of the
        things common to both operations in a centralized place. """
        # WARNING: Tolerance propagation is not yet supported - this is naive!
        tol = max(self.tolerance, other.tolerance)
        count = self.count + other.count
        r = Resistor(0, tol, count)

        parents = []
        # if our parents were same type as us, we can just add a new entry to the list
        if self.history and self.history["operation"] == op:
            parents += list(self.history["parents"])
        else:
            parents.append(self)

        if other.history and other.history["operation"] == op:
            parents += list(other.history["parents"])
        else:
            parents.append(other)

        r.history = {
            "parents": tuple(parents),
            "operation": op
        }

        return r

    def series(self, other):
        """Create a new composite resistor by placing this resistor in series with other"""
        r = self.merge(other, SERIES)
        r.ohms = self.ohms + other.ohms
        r.depth = self.depth + other.depth
        return r

    def parallel(self, other):
        """Create a new composite resistor by placing this resistor in parallel with other"""
        r = self.merge(other, PARALLEL)
        r.ohms = 0
        if self.ohms != 0 and other.ohms != 0:
            r.ohms = 1 / ((1/self.ohms) + (1/other.ohms))
        r.depth = max(self.depth, other.depth)
        return r

    def __add__(self, other):
        """Create a new composite resistor by placing this resistor in series with other"""
        return self.series(other)

    def __rmul__(self, other):
        """Create a new composite resistor by creating `other` copies of self, in series"""
        return self.__mul__(other)

    def __mul__(self, other):
        """Create a new composite resistor by creating `other` copies of self, in series"""
        if type(other) != type(0) or other <= 0:
            return NotImplemented
        r = self
        for i in range(other-1):
            r += self
        return r

    def __or__(self, other):
        """Create a new composite resistor by placing this resistor in parallel with other"""
        return self.parallel(other)

    def __rrshift__(self, other):
        """Create a new composite resistor by creating `other` copies of self, in parallel"""
        return self.__rshift__(other)

    def __rshift__(self, other):
        """Create a new composite resistor by creating `other` copies of self, in parallel"""
        if type(other) != type(0) or other <= 0:
            return NotImplemented
        r = self
        for i in range(other-1):
            r |= self
        return r


    # -------------- Comparisons -----------------
    def __len__(self):
        return self.count

    def __lt__(self, other):
        return self.ohms < other.ohms

    def __gt__(self, other):
        return self.ohms > other.ohms

    def __eq__(self, other):
        """NOTE: This defines *equivalent* resistors to be *equal*!
        This might not be the behavior we'd like long term"""
        return self.ohms == other.ohms

    def __hash__(self):
        # BUG: This will return same hashes for *equivalent* but not *equal*
        # resistors. For example, a 10 + 20 resistor and 12 + 18 resistor.
        # To fix this, need to track info about parents (maybe their hashes)
        return hash( (self.ohms, self.tolerance, self.count, self.depth) )

    # -------------- Strings ---------------------
    def algebraic(self):
        """Return an algebraic string representation of this resistor, e.g.
        (100Ω + 10Ω) | (20Ω + 20Ω)"""

        if not self.history:
            return f"{self.shortOhms()}Ω"

        sym = {PARALLEL: " | ", SERIES: " + "}
        pcs = [p.algebraic() for p in self.history["parents"]]
        op = self.history["operation"]
        return f"({sym[op].join(pcs)})"

    def resistance(self):
        """Return a succinct string representing the equivalent resistance of
        this resistor, e.g. '23.6KΩ'
        """
        return f"{self.shortOhms()}Ω"

    def primitive(self):
        """Return a string representation of this resistor as if it were a
        single primitive resistor, e.g. '-(23.6KΩ)-'
        """
        return f"-({self.resistance()})-"

    def summary(self):
        """Return a succinct string summarizing this resistor's key properties,
        e.g. '<23.6KΩ:n5:d1>'
        """
        return f"<{self.resistance()}:n{self.count}:d{self.depth}>"

    def schematic(self, showEquivalent=False):
        """Return a string representation of this resistor's internal structure
        as a text-based circuit diagram. """
        return str(Schematic(self, showEquivalent))

    def colorCode(self):
        """Return a string representation of the the equivalent color code of
        this resistor."""

        return NotImplemented

    def __str__(self):
        return f"<{self.resistance()} ±{self.tolerance}%>"

    def __repr__(self):
        # TODO: Revise this to be of the form ((100Ω + 10Ω) | (20Ω + 10Ω)) = <XXΩ:n5:d3>
        return f"{self.algebraic()} = {self.summary()}"

        # return f"{{ohms: {self.shortOhms()}, tolerance: {self.tolerance}, count: {self.count}, depth: {self.depth}}}"

    ########################################################################
    #                         Other methods
    ########################################################################

    def shortOhms(self):
        """Return a human-readable shortened form of the number of ohms.

        Format:
          * > 999e24:  X.XXE+XX
          * > 1e3:     XM
                       X.XXM
                       XX.XXM
                       XXX.XM
          * >= 0:      X
                       X.XX
         Note: max width is 6 characters for reasonable resistances
        """
        suffixes = {
            "Y": 10**24, "Z": 10**21, "E": 10**18, "P": 10**15,
            "T": 10**12, "G": 10**9,  "M": 10**6,  "K": 10**3
        }
        ohms = self.ohms

        # > 999Y ohm
        if ohms > 999 * suffixes["Y"]:
            return "%.2E" % ohms

        # 1K ohms to 999T ohms
        for suffix, magnitude in suffixes.items():
            if ohms > magnitude:
                num = ohms / magnitude
                # Whole numbers don't need fractional parts
                if isInteger(num):
                    return f"{round(num)}{suffix}"
                elif num >= 100:
                    return f"{num:.1f}{suffix}"
                else:
                    return f"{num:.2f}{suffix}"

        # < 1K ohms
        if isInteger(ohms):
            return f"{round(ohms)}"
        return f"{ohms:.2f}"

    def isPrimitive(self):
        """Return True iff this resistor is a primitive resistor"""
        return self.count == 1

def isInteger(x, tol=0.0001):
    """Returns true if the fractional part of an integer is less than a tolerance"""
    diff = x - round(x)
    return abs(diff) < tol
