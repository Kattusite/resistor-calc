from .neighbors import Neighbors, lineChars

class Buffer:
    """Buffer defines a 2D array of characters to be used to create text-based
    circuit schematics, and a variety of related helper functions."""

    def __init__(self, w, h):
        self.w = w
        self.h = h
        self.midX = self.w // 2
        self.midY = self.h // 2
        self.buf = [[" " for x in range(w)] for y in range(h)]

    @classmethod
    def fromString(cls, s):
        lines = s.split("\n")
        lens = [len(ln) for ln in lines]
        w = max(lens)
        h = len(lines)
        buf = cls(w, h)
        for y, ln in enumerate(lines):
            for x, c in enumerate(ln):
                buf.buf[y][x] = c
        return buf

    def __str__(self):
        rows = ["".join(r) for r in self.buf]
        return "\n".join(rows)

    def __repr__(self):
        return self.__str__()

    def __add__(self, other):
        return self.concat(other)

    def concat(self, other, center=True):
        """Concatenate self and other horizontally, returning a new, wider buffer.
        The height is the max of the input heights. If center is True,
        the buffers will be vertically centered. Otherwise, they will be top-aligned."""

        newW = self.w + other.w
        newH = max(self.h, other.h)
        buf = Buffer(newW, newH)

        y1, y2 = 0,0
        if center:
            y1 = buf.midY - self.midY
            y2 = buf.midY - other.midY

        buf.set(0, y1, self)
        buf.set(self.w, y2, other)

        return buf

    def display(self):
        print(str(self))

    def set(self, xi,yi, buf):
        """Fill the contents of buf into self starting at x,y."""

        if type(buf) == type(""):
            buf = Buffer.fromString(buf)

        for y, ln in enumerate(buf.buf):
            for x, c in enumerate(ln):
                if yi + y < len(self.buf) and xi + y < len(self.buf[0]):
                    self.buf[yi+y][xi+x] = buf.buf[y][x]

    def sub(self, x0, y0, x1, y1):
        """Get a sub-buffer from x0,y0 to x1,y1"""
        # We don't need this to make schematics.
        return NotImplemented

    def line(self, x0, y0, x1, y1):
        """Draw a line connecting x0,y0 and x1,y1.
        The line first moves across and then up if needed.
        """
        # TODO: Make it so that wires check what was already there, and add
        # junctions if overwrites would occur.
        # This also negates the need for the corner case.

        w, h = x1-x0, y1-y0
        for x in range(x0, x1+1):
            self.buf[y0][x] = "-"

        for y in range(y0+1, y1+1):
            self.buf[y][x1] = "-"

        # Draw a corner if needed
        if w > 0 and h > 0:
            self.buf[y0][x1] = "-"

    def isLine(self, x,y):
        """Return true if the character at x,y is a line-drawing character"""
        # Consider the edges of the buffer to allow horizontal connections (but not vertical)
        if x < 0 or x >= self.w:
            return True
        if y < 0 or y >= self.h:
            return False
        c = self.buf[y][x]
        return c in lineChars

    def areNeighborsLines(self, x, y):
        """Return an object with .left, .right, .above, .below properties, each
        a bool indicating whether that neighbor of square x,y is a line. """

        return Neighbors(left  = self.isLine(x-1,y), right = self.isLine(x+1,y),
                         above = self.isLine(x,y-1), below = self.isLine(x,y+1))

    def connectLines(self, fancy=True):
        """Convert all naive line segments (denoted "-") into smartly drawn ones,
        using box drawing characters.

        If fancy is false, use simple ascci (-+|) instead"""

        for y, ln in enumerate(self.buf):
            for x, c in enumerate(ln):
                if not self.isLine(x,y):
                    continue

                ns = self.areNeighborsLines(x,y)
                s = ns.fancyString()
                if not fancy:
                    s = ns.simpleString()
                self.buf[y][x] = s
