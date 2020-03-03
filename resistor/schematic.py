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

# no need to track terminals - just track width/height, and assume terminals are always at midpoints


class Schematic:

    # For operations, we need:
    # 1) create schematic from primitive resistor
    # 2) connect schematics in series
    # 3) connect schematics in parallel

    # Also need some general helpers for 2d char arrays

    def __init__(self, resistor):

        op = "" if not resistor.history else resistor.history["operation"]

        # base case
        s = ""
        if not resistor.history:
            s = f"-({resistor.shortOhms()}Ω)-"
        elif op == PARALLEL:
            # recursively fetch schematics of children

            # figure out max width & total height, allocate new buffer

            # allocate each child its requested height, plus 1 padding between

            # place children into buffer one at a time, centering them in a row

        else # op == SERIES:
            # recursively fetch schematics of children

            # figure out max height & total width, allocate new buffer

            # allocate each child its requested width, plus 1 padding between

            # place children into buffer one at a time, centering them vertically






        self.width = w
        self.height = h

        self.text = [
            [x, y, z],
            [a, b, c],
            [d, e, f]
        ] # W x H
