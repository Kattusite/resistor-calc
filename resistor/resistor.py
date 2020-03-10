"""resistor.py defines the Resistor class, which defines a collection of useful
ways to compose and work with electrical resistors.

Terminology:
  * A "primitive" resistor is one consisting of just a single physical component
  * A "composite" or "complex" resistor consists of several smaller components,
    primitive or composite, arranged in series and/or parallel.

TODO:
  * Resistor color code handling / representation
  * Track breadth as well as depth (max parallelism)
  * Standardize API + docs
    - Convert mentions of "self" to "this Resistor"
  * Decide what to do when no tolerance/temp coeff is provided?
    - Provide a reasonable default or set to None?
    - If set to None, what should fns like minOhms() that require it do?
    -- Exception? Also None?
    - Also what about color code?
"""

from units import Units
from .schematic import Schematic
from .colors import Colors
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
    #                         Constructor
    ########################################################################

    def __init__(self, ohms, tolerance=1, tempCoefficient=100):
        if ohms < 0:
            raise ValueError(f"ohms cannot be negative! ({ohms} < 0)")
        if tolerance < 0:
            raise ValueError(f"tolerance cannot be negative! ({tolerance} < 0)")

        self.__ohms = ohms
        """The equivalent resistance of this Resistor, as a number of ohms."""

        self.__tolerance = tolerance
        """The tolerance of this Resistor, in percentage points."""

        self.__tempCoefficient = tempCoefficient
        """The temperature coefficient of this Resistor, in ppm/deg C."""

        self.__depth = 1
        """The number of primitive resistors on this Resistor's longest internal path."""

        self.__breadth = 1
        """The number of primitive resistors in this Resistor's widest parallel branch."""

        self.__count = 1
        """The total number of primitive resistors in this Resistor's internal structure."""



        self.history = None # TODO: Rename to self.components, add a self.arrangment to store PARALLEL/SERIES
        self.__components  = None # this resistor's *direct* subcomponents
        self.__arrangement = None # how those subcomponents are arranged

    ########################################################################
    #                          Properties
    ########################################################################

    # TODO: Do this with properties as discussed here:
    # https://stackoverflow.com/questions/10929004/how-to-restrict-setting-an-attribute-outside-of-constructor

    @property
    def ohms(self):
        """The equivalent resistance of this Resistor, in ohms."""
        return self.__ohms

    @ohms.setter
    def ohms(self, x):
        raise TypeError("Cannot set fields of an immutable Resistor.")

    @property
    def R(self):
        """The equivalent resistance of this Resistor, in ohms.

        Alias for self.ohms
        """
        return self.ohms

    @R.setter
    def R(self, x):
        raise TypeError("Cannot set fields of an immutable Resistor.")

    @property
    def depth(self):
        """The number of resistors on this Resistor's longest internal path."""
        return self.__depth

    @depth.setter
    def depth(self, x):
        raise TypeError("Cannot set fields of an immutable Resistor.")

    @property
    def breadth(self):
        """The number of resistors in this Resistor's widest internal parallel branch."""
        return self.__breadth

    @breadth.setter
    def breadth(self, x):
        raise TypeError("Cannot set fields of an immutable Resistor.")

    @property
    def tolerance(self):
        """The tolerance of this resistor, in percentage points."""
        return self.__tolerance

    @tolerance.setter
    def tolerance(self, x):
        raise TypeError("Cannot set fields of an immutable Resistor.")

    @property
    def temperatureCoeffcient(self):
        """The temperature coefficient of this resistor, in ppm/deg C."""
        return self.__tempCoefficient

    @temperatureCoeffcient.setter
    def temperatureCoeffcient(self, x):
        raise TypeError("Cannot set fields of an immutable Resistor.")

    @property
    def tcr(self):
        """The temperature coefficient of this resistor, in ppm/deg C.

        Alias for self.temperatureCoeffcient"""
        return self.temperatureCoeffcient

    @tcr.setter
    def tcr(self, x):
        raise TypeError("Cannot set fields of an immutable Resistor.")

    ########################################################################
    #                    Creators (Operations)
    ########################################################################

    def __merge(self, other, op):
        """Return a new Resistor combining common features of self and other.

        A helper function for series/parallel. This helper does all of the
        things common to both operations in a centralized place.
        """

        # WARNING: Tolerance propagation is not yet supported - this is naive!
        r = Resistor(0)
        r.tol = max(self.tolerance, other.tolerance)
        r.__count = self.__count + other.__count

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
        """Return a new composite Resistor comprised of self and other in series."""
        r = self.__merge(other, SERIES)
        r.__ohms = self.ohms + other.ohms
        r.__depth = self.depth + other.depth
        return r

    def __add__(self, other):
        """Return a new composite Resistor comprised of self and other in series.

        Alias for self.series(other).
        """
        return self.series(other)

    def parallel(self, other):
        """Return a new composite Resistor comprised of self and other in parallel."""
        r = self.__merge(other, PARALLEL)
        r.__ohms = 0
        if self.ohms != 0 and other.ohms != 0:
            r.__ohms = 1 / ((1/self.ohms) + (1/other.ohms))
        r.__depth = max(self.depth, other.depth)
        return r

    def __or__(self, other):
        """Return a new composite Resistor comprised of self and other in parallel.

        Alias for self.parallel(other).
        """
        return self.parallel(other)

    def __mul__(self, n):
        """Return a new composite resistor comprised of n serial copies of self."""
        # Attempt to cast n to an int
        if "__int__" not in dir(n) or int(n) <= 0:
            return NotImplemented
        r = self
        for i in range(int(n)-1):
            r += self
        return r

    def __rmul__(self, n):
        """Return a new composite resistor comprised of n serial copies of self.

        Alias of self.__mul__(n).
        """
        return self.__mul__(n)

    def __rshift__(self, n):
        """Return a new composite resistor comprised of n parallel copies of self."""
        # Attempt to cast n to an int
        if "__int__" not in dir(n) or int(n) <= 0:
            return NotImplemented
        r = self
        for i in range(int(n)-1):
            r |= self
        return r

    def __rrshift__(self, n):
        """Return a new composite resistor comprised of n parallel copies of self.

        Alias of self.__rshift__(n).
        """
        return self.__rshift__(n)

    def toPrimitive(self):
        """Return a new primitive Resistor with equal resistance to self."""
        return Resistor(self.ohms)

    def clamped(self):
        """Return a new primitive Resistor with equal resistance to 3sigfigs of self."""
        # TODO: Implement by calling Resistor(int(self.colorCode(type=number,graphical=False))
        return NotImplemented

    def __trunc__(self):
        """Return a new primitive Resistor with equal resistance to 3sigfigs of self.

        Alias for self.clamped().
        """
        return self.clamped()

    def __round__(self):
        return NotImplemented

    def __ceil__(self):
        return NotImplemented

    def __floor__(self):
        return NotImplemented

    def __invert__(self):
        """Return a new composite resistor, swapping all series/parallel connections."""
        return NotImplemented

    ########################################################################
    #                  Observers (Comparison)
    ########################################################################

    def __lt__(self, other):
        """Return True iff self.ohms < other.ohms."""
        return self.ohms < other.ohms

    def __le__(self, other):
        """Return True iff self.ohms <= other.ohms."""
        return self.ohms <= other.ohms

    def __gt__(self, other):
        """Return True iff self.ohms > other.ohms."""
        return self.ohms > other.ohms

    def __ge__(self, other):
        """Return True iff self.ohms >= other.ohms."""
        return self.ohms >= other.ohms

    def __eq__(self, other):
        """Return True iff self.ohms == other.ohms.

        Note: This means that two resistors are equal so long as their
        equivalent resistances are equal, regardless of internal composition.
        """
        return self.ohms == other.ohms

    def __ne__(self, other):
        """Return True iff self.ohms != other.ohms.

        Note: This means that two resistors are not equal so long as their
        equivalent resistances are not equal, regardless of internal composition.
        """
        return self.ohms != other.ohms

    def __hash__(self):
        """Return a hash of this Resistor.

        Hashes will be equal if two resistors have the same internal structure.
        """
        # WARNING: We don't hash the operation used to combine our history,
        # so we might say that hash(100 | 200) == hash(100 + 200)
        # --> Not sure if this would be an issue, since equivalent resistances
        #     would necessarily be different.
        # --> Only case I can think of that might cause issues is (0 | 0) == (0 + 0)

        myHash = hash((self.ohms, self.tolerance, self.__count, self.depth, self.breadth))
        if self.isPrimitive():
            return myHash

        componentHashes = tuple([hash(r) for r in self.history])
        return hash((myHash, componentHashes))

    ########################################################################
    #                  Observers (Boolean)
    ########################################################################

    def isPrimitive(self):
        """Return True iff this Resistor is a primitive resistor."""
        return self.__count == 1

    ########################################################################
    #                  Observers (Numerical)
    ########################################################################

    def minOhms(self):
        """Return the lowest tolerable number of ohms for this Resistor."""
        return self.ohms - (self.ohms * (self.tolerance / 100))

    def maxOhms(self):
        """Return the highest tolerable number of ohms for this Resistor."""
        return self.ohms + (self.ohms * (self.tolerance / 100))

    def ohmsRange(self):
        """Return the uncertainty range of ohms for this Resistor.

        The uncertainty range is returned as a tuple (self.minOhms(), self.maxOhms()).
        """
        delta = (self.ohms * (self.tolerance/100))
        return (self.ohms - delta, self.ohms + delta)

    def numPrimitives(self):
        """Return the number of primitive resistors in this Resistor's internal structure."""
        return self.__count

    def __len__(self):
        """Return the number of primitive resistors used in this Resistor.

        Alias for self.numPrimitves().
        """
        return self.numPrimitives()

    ########################################################################
    #                  Observers (Electrical)
    ########################################################################

    def current(self, V):
        """Return the current passing through this Resistor under a voltage V.

        Parameters:
        * V, as a number of volts.

        Returns a current, as a number of amps.
        """
        return V / self.ohms

    def voltage(self, I):
        """Return the voltage drop over this Resistor given a current I.

        Parameters:
        * I, as a number of amps.

        Returns a voltage, as a number of volts.
        """
        return I * self.ohms

    def power(self, I, volts=False):
        """Return the power dissipated by this Resistor given a current I.

        Parameters:
        * I, as a number of amps.
        * volts: if True, interpret I as the voltage drop in volts instead.

        Returns a power, as a number of watts.
        """
        if not volts:
            return I * I * self.ohms
        V = I
        return (V * V) / self.ohms

    def energy(self, I, t, volts=False):
        """Return the energy disspated over a time t by this Resistor given a current I.

        Parameters:
        * I, as a number of amps.
        * t, as a number of seconds.
        * volts: if True, interpret I as the voltage drop in volts instead.

        Returns an energy, as a number of joules.
        """
        return self.power(I, volts) * t

    def wireResistivity(self,L,A):
        """Return the resistivity of an equivalent wire of length L and cross-section A.

        Assuming this resistor is modeled by a wire of a given length and
        cross-sectional area, return the resistivity the wire must have in order
        to have the same equivalent resistance as this Resistor.

        Parameters:
        * L: wire length, as a number of meters.
        * A: cross-sectional area of wire, as a number of square meters.

        Return the resistivity, as a number of ohm-meters.
        """
        return (self.ohms * A) / L

    def wireLength(self,rho,A):
        """Return the length of an equivalent wire of resistivity rho and cross-section A.

        Assuming this resistor is modeled by a wire of a given resistivity and
        cross-sectional area, return the length the wire must have in order
        to have the same equivalent resistance as this Resistor.

        Parameters:
        * rho: resistivity, as a number of ohm-meters.
        * A: cross-sectional area of wire, as a number of square meters.

        Return the wire length, as a number of meters.
        """
        return (self.ohms * A) / rho

    def wireArea(self,rho,L):
        """Return the length of an equivalent wire of resistivity rho and length L.

        Assuming this resistor is modeled by a wire of a given resistivity and
        length, return the cross-sectional area the wire must have in order
        to have the same equivalent resistance as this Resistor.

        Parameters:
        * rho: resistivity, as a number of ohm-meters.
        * L: wire length, as a number of meters.

        Return the cross-sectional area, as a number of square meters.
        """
        return (L * rho) / self.ohms

    def wheatstone(self, r1, r2):
        """Return a new Resistor completing the Wheatstone bridge formed by this Resistor, r1 and r2.

        Parameters:
        * self: r0 in the diagram below
        * r1, as shown in the diagram below
        * r2, as shown in the diagram below:
             |
            / \
           a   b
          /     \
         +---V---+
          \     /
           c   ?
            \ /
             |
        """
        # TODO: Figure out which resistors are arugments.
        return NotImplemented


    ########################################################################
    #                  Observers (String)
    ########################################################################

    def resistance(self):
        """Return a succinct string representing the resistance of this Resistor.

        e.g. '23.6KΩ'
        """
        return str(Units.ohms(self.ohms))

    def algebraic(self):
        """Return an algebraic string representation of this resistor, e.g.
        (100Ω + 10Ω) | (20Ω + 20Ω)"""

        if self.isPrimitive():
            return self.resistance()

        sym = {PARALLEL: " | ", SERIES: " + "}
        pcs = [p.algebraic() for p in self.history["parents"]]
        op = self.history["operation"]
        return f"({sym[op].join(pcs)})"

    def primitive(self):
        """Return a string representation of this resistor as if it were a
        single primitive resistor, e.g. '-(23.6KΩ)-'
        """
        return f"-({self.resistance()})-"

    def summary(self):
        """Return a succinct string summarizing this resistor's key properties,
        e.g. '<23.6KΩ:n5:d1>'
        """
        return f"<{self.resistance()}:n{self.numPrimitives()}:d{self.depth}:b{self.breadth}>"

    def schematic(self, showEquivalent=False):
        """Return a string representation of this resistor's internal structure
        as a text-based circuit diagram. """
        return str(Schematic(self, showEquivalent))

    def colorCode(self, ncolors=5, style="num", succinct=False, background=False):
        """Return a string representation of the the equivalent color code of
        this resistor."""
        if ncolors not in [3,4,5,6]:
            raise ValueError("Resistor color codes are only defined for 3, 4, 5, or 6 colors.")

        colors = Colors.fromResistor(self, ncolors=5)
        diagram = Colors.resistorDiagram(colors, style=style, succinct=succinct, background=background)
        return diagram

    def __str__(self):
        return f"<{self.resistance()} ±{self.tolerance}%>"

    def __repr__(self):
        # TODO: Decide what the best format for this would be
        return f"<Resistor ({self.resistance()}) n{self.numPrimitives()}:d{self.depth}:b{self.breadth}>"
        #return f"{self.algebraic()} = {self.summary()}"


    ########################################################################
    #                  Observers (Other)
    ########################################################################

    def components(self):
        """Return a list of the primitive Resistors making up this Resistor."""
        return NotImplemented

    def structure(self):
        """Return a representation of this Resistor's internal structure."""
        return NotImplemented

    ########################################################################
    #                        Mutators
    ########################################################################

    ########################################################################
    #                     Other methods
    ########################################################################
