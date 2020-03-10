# TODO: Provide methods for converting between units
# i.e. 100V / 50A = 2Ω

from .quantity import Quantity
from .const import unitNames
from .math_helpers import *

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
