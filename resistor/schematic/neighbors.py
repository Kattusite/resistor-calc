dirs = ["left", "right", "above", "below"]

lineChars = (
    "-+|"  +  # simple ascii
    "─│"   +  # straight lines
    "┌┐└┘" +  # corners
    "├┤┬┴" +  # T junctions
    "┼"    +  # fancy + junction
    "╴╵╶╷"    # terminals (don't render great)
)

fancyLookup = {
    "lrab": "", # order of the directions
    "0000": " ",
    # 1 wire only
    # ordinarily these would be terminals, but they render poorly
    # so we use full length standard lines instead.
    "1000": "─",
    "0100": "─",
    "0010": "│",
    "0001": "│",

    # 2 wires only
    "0011": "│",
    "1100": "─",
    "0101": "┌",
    "0110": "└",
    "1001": "┐",
    "1010": "┘",

    # 3 wires only
    "0111": "├",
    "1011": "┤",
    "1101": "┬",
    "1110": "┴",

    # 4 wires
    "1111": "┼",
}

class Neighbors:

    def __init__(self, left=False, right=False, above=False, below=False):
        self.left = left
        self.right = right
        self.above = above
        self.below = below

    def __len__(self):
        ls = [1 for d in dirs if getattr(self, d)]
        return sum(ls)

    def binaryString(self):
        cs = ["1" if getattr(self, d) else "0" for d in dirs]
        return "".join(cs)

    def simpleString(self):
        if len(self) == 0:
            return " "
        if (self.left or self.right) and not (self.above or self.below):
            return "-"
        if (self.above or self.below) and not (self.left or self.right):
            return "|"
        return "+"

    def fancyString(self):
        return fancyLookup[self.binaryString()]

    def __str__(self):
        return self.fancyString()
