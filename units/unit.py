# TODO: Provide methods for converting between units
# i.e. 100V / 50A = 2Ω

from .quantity import Quantity
from .const import unitNames

import math

##############################################################################
#                         Helper Functions
##############################################################################

def isInteger(x, tol=0.0001):
    """Returns true if the fractional part of an integer is less than a tolerance"""
    diff = x - round(x)
    return abs(diff) < tol

def magnitude(x):
    """Return the order of magnitude of x, as both an exponent and a power of 10"""
    e = math.floor(math.log10(x))
    return (e, 10 ** e)

    # BUG: Something wrong:
    #  ┌───(100Ω)───(10Ω)───┐
    # ─┤                    ├─ == ─(52.400000000000006Ω)─
    #  └───────(100Ω)───────┘
    # truncate(52.38095238095239) is buggy
def truncate(x, sigfigs=3):
    """Truncate x to the given number of sigfigs."""
    if x == 0:
        return 0

    exp, mag = magnitude(x)

    # Bring x to range [1, 10)
    x /= mag

    # Shift left by `sigfigs` digits
    scale = 10 ** (sigfigs-1)
    x *= scale

    # Truncate all trailing digits to the right.
    x = round(x)

    # Shift right by `sigfigs` digits
    x /= scale

    # Restore x to original range
    x *= mag

    # Fix precision errors
    # exp+1 of the sigfigs are integers. drop the fractional part
    if exp >= 0:
        x = round(x, ndigits=sigfigs-(exp+1))

    return x

##############################################################################
#                            Unit Class
##############################################################################

class Unit():
    """A particular SI unit that measures a specific physical property.

    e.g.
    """

    suffixes = {
        "Y": 10**24,  "Z": 10**21,  "E": 10**18,  "P": 10**15,
        "T": 10**12,  "G": 10**9,   "M": 10**6,   "K": 10**3,    "":  10**0,
        "m": 10**-3,  "μ": 10**-6,  "n": 10**-9,  "p": 10**-12,
        "f": 10**-15, "a": 10**-18, "z": 10**-21, "y": 10**-24,
    }

    def __init__(self, abbr, property=None):
        """Return a new SI unit with given base abbreviation and measured property"""
        self.abbr = abbr
        self.property = property
        self.name = unitNames[abbr] if abbr in unitNames else abbr

    def __call__(self, *args):
        """Shorthand for Quantity(args[0], self)."""
        return Quantity(*args, self)

    def format(self, x, sigfigs=3):
        """Return a formatted string representation of x in units of self.

        e.g. watts.format(455_000) => "455kW"
             amps.format(0.050)    => "50mA"

        Format:
          * > 999e24:  X.XXE+XXU
          * > 1e3:     XMU
                       X.XXMU
                       XX.XXMU
                       XXX.XMU
          * >= 0:      XU
                       X.XXU
         Note: max width is U characters for reasonably sized x
        """
        # Special case: zero
        if x == 0:
            return f"0{self.abbr}"

        # Note the sign, and convert to positive number
        sign = "-" if x < 0 else ""
        x = abs(x)

        # Really big numbers: use scientific notation
        default = f"{x:.2e}{self.abbr}"
        if x > 999 * self.suffixes["Y"]:
            return default

        for suffix, magnitude in self.suffixes.items():
            if x > magnitude:
                num = x / magnitude

                num = truncate(num, sigfigs)

                if isInteger(num):
                    return f"{sign}{round(num)}{suffix}{self.abbr}"
                else:
                    return f"{sign}{num}{suffix}{self.abbr}"

        # Really small numbers: use scientific notation
        return f"{sign}{x:.2e}{self.abbr}"
