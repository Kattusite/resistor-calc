"""resistor.py defines the Resistor class, which defines a collection of useful
ways to compose and work with electrical resistors.

TODO:
  * Resistor color code handling / representation
  * ASCII Schematic of internal structure of composite resistors
"""

SERIES = "series"
PARALLEL = "parallel"

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

    def __len__(self):
        return self.count

    def __add__(self, other):
        """Create a new composite resistor by placing this resistor in series with other"""
        ohms = self.ohms + other.ohms
        tol  = max(self.tolerance, other.tolerance)
        count = self.count + other.count
        depth = self.depth + other.depth
        r = Resistor(ohms, tol, count, depth)
        r.history = {
            "parents": (self, other),
            "operation": SERIES
        }
        return r

    def __or__(self, other):
        """Create a new composite resistor by placing this resistor in parallel with other"""
        ohms = 0
        if self.ohms != 0 and other.ohms != 0:
            ohms = 1 / ((1/self.ohms) + (1/other.ohms))
        tol  = max(self.tolerance, other.tolerance)
        count = self.count + other.count
        depth = max(self.depth, other.depth)
        r = Resistor(ohms, tol, count, depth)
        r.history = {
            "parents": (self, other), # NOTE: If one/both of our parents was parallel we can condense tree structure
            "operation": PARALLEL
        }
        return r


    # -------------- Comparisons -----------------
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
    def __str__(self):
        return f"<{self.shortOhms()}Ω ±{self.tolerance}%>"

    def __repr__(self):
        return f"{{ohms: {self.shortOhms()}, tolerance: {self.tolerance}, count: {self.count}, depth: {self.depth}}}"

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
                if num == round(num):
                    return f"{round(num)}{suffix}"
                elif num >= 100:
                    return f"{num:.1f}{suffix}"
                else:
                    return f"{num:.2f}{suffix}"

        # < 1K ohms
        if ohms == round(ohms):
            return f"{round(ohms)}"
        return f"{ohms:.2f}"

    def isPrimitive(self):
        """Return True iff this resistor is a primitive resistor"""
        return self.count == 1

    def colorCode(self):
        """Return the equivalent color code of this resistor."""
        return NotImplemented

    def schematic(self):
        """Return an ASCII schematic of this resistor's internal components"""
        # TODO: Wildly buggy. Should treat as 2d arrays of chars getting stitched
        # together, not as strings.

        # Base case:
        if self.history is None:
            # BUG: Should be a fixed-width block. must pad w/ whitespace
            return f"--({self.shortOhms()}Ω)--"

        if self.history["operation"] == SERIES:
            L = self.history["parents"][0].schematic()
            R = self.history["parents"][1].schematic()
            return f"{L}{R}"

        else: # if self.history["operation"] == PARALLEL
            L = self.history["parents"][0].schematic()
            R = self.history["parents"][1].schematic()
            return f" +{L}+\n-+       +-\n +{R}+\n"
