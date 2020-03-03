# The logic for schematic will likely require lots of new helpers
# I imagine the workflow might be something like:

# 1) Parse the ancestor tree
# 2) Condense ancestor tree into series of parallels.
#       (i.e. collapse all parallels into flat structures)
# 3) For each parallel:
#   3a) Figure out the width of the longest member
#   3b) Print each member in its own row (into a buffer)
#       Be sure to center the elements of that row and pad with wires "----"
#   3c) Figure out where the terminals of the entire block would be
#        so we know where to connect up to the next block
# 4) ...?
# 5) This whole thing obviously needs to be recursive, since parallels can be
#    nested inside series, inside parallel, inside series, inside....
#
#
# We will likely need to treat schematics as 2D floating buffers of characters, and
# keep track of their bounding boxes and terminals

from ..const import SERIES, PARALLEL
from .buffer import Buffer

# no need to track terminals - just track width/height, and assume terminals are always at midpoints

# Prove by induction that heights will always be odd.

class Schematic:

    # For operations, we need:
    # 1) create schematic from primitive resistor
    # 2) connect schematics in series
    # 3) connect schematics in parallel

    def __init__(self, resistor, showEquivalent=False):
        """Create a new Schematic of the provided resistor.
        If showEquivalent is True, also include a schematic of the simplified
        equivalent resistor."""

        self.resistor = resistor
        self.showEquivalent = showEquivalent

        op = "" if not resistor.history else resistor.history["operation"]
        parents = () if not resistor.history else resistor.history["parents"]

        # base case
        s = ""
        if not resistor.history:
            self.buf = Buffer.fromString(f"-({resistor.shortOhms()}Ω)-")
        elif op == PARALLEL:
            # Drawing something like:
            #  +--(200)--+
            #  |         |
            # -+--(100)--+-
            #  |         |
            #  +--(200)--+

            # recursively fetch schematics of children
            parentSchematics = [Schematic(p) for p in parents]

            # figure out max width & total height, allocate new buffer
            maxW = max([schem.buf.w for schem in parentSchematics])
            totH = sum([schem.buf.h for schem in parentSchematics])
            n = len(parentSchematics)

            # 6 H padding for -+- ... -+-
            # 1 W padding for each of the n-1 gaps between parentSchematics
            self.buf = Buffer(maxW + 6, totH + n - 1)

            # place children into buffer one at a time, centering them in their row
            y = 0
            for schem in parentSchematics:
                # draw a wire through the vertical midline of this schematic
                midY = schem.buf.midY + y
                self.buf.line(2, midY, self.buf.w-3, midY)

                # fill in the schematic in its position, centered.
                midX = self.buf.midX
                self.buf.set(midX - schem.buf.midX, y, schem.buf)
                y += schem.buf.h + 1

            # Draw the vertical wires connecting the parallel tracks
            topY = parentSchematics[0].buf.midY
            botY = (self.buf.h - 1) - parentSchematics[-1].buf.midY
            midY = self.buf.midY

            left = 1
            right = self.buf.w - 2
            self.buf.line(left, topY, left, botY)
            self.buf.line(right, topY, right, botY)

            # Draw the far left input and far right output wires
            self.buf.set(left-1, midY, "--")
            self.buf.set(right, midY, "--")

        else: # op == SERIES:
            # Drawing something like:
            #     +--(200)--+
            #   --+         +--(200)----(400)--
            # -   +--(100)--+-


            # recursively fetch schematics of children
            parentSchematics = [Schematic(p) for p in parents]

            # figure out max height & total width, allocate new buffer
            # figure out max width & total height, allocate new buffer
            maxH = max([schem.buf.h for schem in parentSchematics])
            totW = sum([schem.buf.w for schem in parentSchematics])
            n = len(parentSchematics)

            # 2 padding for - ... -, plus 1 padding for each gap btwn schems
            self.buf = Buffer(totW + (n - 1) + 2, maxH)

            # draw a horizontal center line
            midY = self.buf.midY
            self.buf.line(0, midY, self.buf.w-1, midY)

            # place children into buffer one at a time, centering them vertically
            x = 1
            for schem in parentSchematics:
                midY = self.buf.midY - schem.buf.midY
                self.buf.set(x, midY, schem.buf)
                x += schem.buf.w + 1

        # add in fancy line connections
        self.buf.connectLines(fancy=True)

        # Create a second buffer to store equivalence information
        self.buf2 = Buffer.fromString(f" == {self.resistor.primitive()}")
        self.buf2.connectLines(fancy=True)

        self.combined = self.buf + self.buf2

    def toString(self, showEquivalent=False):
        if showEquivalent:
            return str(self.combined)
        return str(self.buf)

    def __str__(self):
        return self.toString(self.showEquivalent)

    def __repr__(self):
        return str(self)
