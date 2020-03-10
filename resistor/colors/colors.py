# Experimental - not really well designed or organized yet
# TODO: Scrap almost the whole file and reorganize from the ground up

from collections import OrderedDict

from units.math_helpers import truncate, magnitude
from .color import Color
from .diagram import Diagram
from .const import ENDC, esc, esc8, esc24x

# The 4bit colors are really poorly matched
# the worst offender is brown, which is really bright magenta
# TODO: Revise per more formal spec at https://en.wikipedia.org/wiki/Electronic_color_code#Resistors
# TODO: This isn't an ideally sensible constructor API for resistors.
#       We lose what it means to be a pure "Color" by having weird text alternatives
color_defs = OrderedDict({
    "black":  Color("k", "Bk", "blk", "0", esc(30), esc8(  0), esc24x(0x000000)),
    "brown":  Color("n", "Br", "bwn", "1", esc(95), esc8( 94), esc24x(0x663232)),
    "red":    Color("r", "Rd", "red", "2", esc(91), esc8(  9), esc24x(0xff0000)),
    "orange": Color("o", "Or", "orn", "3", esc(31), esc8(214), esc24x(0xff6600)),
    "yellow": Color("y", "Yl", "ylw", "4", esc(93), esc8( 11), esc24x(0xffff00)),
    "green":  Color("g", "Gr", "grn", "5", esc(92), esc8( 10), esc24x(0x34cd32)),
    "blue":   Color("b", "Bl", "blu", "6", esc(34), esc8( 12), esc24x(0x6666ff)),
    "violet": Color("v", "Vi", "vio", "7", esc(35), esc8(129), esc24x(0xcd66ff)),
    "grey":   Color("e", "Gy", "gry", "8", esc(90), esc8(245), esc24x(0x939393)),
    "white":  Color("w", "Wh", "whi", "9", esc(97), esc8( 15), esc24x(0xffffff)),
    "gold":   Color("u", "Au", "gld", "a", esc(33), esc8(178), esc24x(0xcd9932)),
    "silver": Color("s", "Ag", "slv", "b", esc(37), esc8(189), esc24x(0xcac9c9)),
})

class Colors:
    colors=[]
    for _, c in color_defs.items():
        colors.append(c)

    # ================ Define pseudocolors ======================
    # A pseudocolor that renders as nothing.
    NONE = Color(" ", "  ", "   ", " ", "", "", "")

    # A psuedocolor that renders as question marks in ascii/num formats
    UNKNOWN = Color("?", "??", "???", "?", "", "", "")

    # The ANSI escape sequence to stop displaying colored text.
    ENDC = ENDC


    #######################################################################
    #                     Creators (Build Color objects)
    #######################################################################

    @classmethod
    def fromResistor(cls, r, ncolors=5):
        """Return a list Color objects representing the bands in a Resistor's color code."""

        if ncolors not in [3,4,5,6]:
            raise ValueError("Resistor color codes are defined only for 3, 4, 5, or 6 colors.")

        # find order of magnitude mag = max(10**int(e)) s.t. mag < r.ohms
        e, mag = magnitude(r.ohms)
        ohms = truncate(r.ohms / mag, 3)
        ohmStr = f"{ohms:.2f}".replace(".", "") # The 3 MSDs of ohms, as a string

        # get colors for the first three digits of the resistance
        digitColors = [cls.fromDigit(int(ohmStr[i])) for i in [0,1,2]]

        # get color for the order of magnitude
        shift = 1 if ncolors <= 4 else 2 # how many OoM accounted for in digitColors?

        # TODO: What to do if this raises an error? use NONE_COLOR? Propagate error?
        magnitudeColor = cls.fromMagnitude(e - shift)

        # get colors for the resistor's tolerance and temp coefficient
        tolColor = cls.fromTolerance(r.tolerance)
        tempColor = cls.fromTempCoefficient(r.tcr)

        # All color codes have 2 digits, and those w/ 5+ colors have 3 digits
        colors = digitColors[:2]
        if ncolors >= 5:
            colors.append(digitColors[2])

        colors.append(magnitudeColor)

        if ncolors >= 4:
            colors.append(tolColor)

        if ncolors == 6:
            colors.append(tempColor)

        return colors

    @classmethod
    def resistorDiagram(cls, colors, style=Color.COL24, succinct=False, background=False):
        """Return a string representing the resistor color code for the provided colors in the given style."""

        if len(colors) not in [3,4,5,6]:
            raise ValueError("Resistor color codes are defined only for 3, 4, 5, or 6 colors.")

        if style not in colors[0].__dict__:
            raise ValueError(f"Invalid value for argument 'style': {style}")

        diagram = Diagram(colors, style, succinct, background)
        return str(diagram)

    @classmethod
    def fromDigit(cls, n):
        if n < 0 or n > 9:
            raise ValueError
        return cls.colors[n]

    @classmethod
    def fromMagnitude(cls, e):
        if e > 9 or e < -2:
            raise ValueError(f"Resistance magnitudes outside [10**-2, 10**9] have no associated color code! (10**{e})")

        if e == -2:
            return cls.colors[-1]
        elif e == -1:
            return cls.colors[-2]

        return cls.colors[e]

    @classmethod
    def fromTolerance(cls, tol):
        tols = [
            None, 1, 2, None, None,
            0.5, 0.25, 0.10, 0.05, None,
            5, 10
        ]
        if tol not in tols:
            raise ValueError(f"Resistor tolerance of {tol} has no associated color code!")
        i = tols.index(tol)
        return cls.colors[i]

    @classmethod
    def fromTempCoefficient(cls, coeff):
        coeffs = [
            None, 100, 50, 15, 25,
            None, 10, 5, None, None,
            None, None
        ]
        if coeff not in coeffs:
            raise ValueError(f"Resistor temperature coefficient of {coeff} has no associated color code!")
        i = coeffs.index(coeff)
        return cls.colors[i]

    #########################################################################
    #  TODO: Things below here are deprecated, and in need of attention.
    #        They should probably be moved to Color or deleted entirely.
    #########################################################################

    def colorprint(color, *argv):
        print(color, *argv, Colors.ENDC)

    def colorstr(color, s):
        return f"{color}{s}{Colors.ENDC}"

    def start(color):
        print(color,end="")

    def end():
        print(Colors.ENDC,end="")

# ================ Define standard colors ======================
# Define Colors.BLACK, Colors.BROWN, Colors.RED, and so on...
for name, c in color_defs.items():
    setattr(Colors, name.upper(), c)
