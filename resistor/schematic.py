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
