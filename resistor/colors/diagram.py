
"""
Implementation choices:

Option 1)
    Generate the succinct version first, and write a helper function to wrap it
    in box drawing characters.

Option 2)
    Special cases for each

"""

from .color import Color
from .const import BLUE_BG, ENDC

# asciiTemplate = (
#     "   /-------------------\   " +
#     "  |  r | b | g | w |  b |  " +
#     "--|  e | l | r | h |  l |--" +
#     "  |  d | u | n | i |  k |  " +
#     "   \-------------------/   "
# )

# TODO: Add 2 rows (only for ascii2,ascii3)
# TODO: Add 1 col  (for 6-wide)
# colorTemplate = [
#     " ┌────────┐ ",
#     "─┤ 1234 5 ├─",
#     " └────────┘ ",
# ]

templates = {
    3: "123    ",
    4: "123   4",
    5: "1234  5",
    6: "1234 56",
}

def join(pcs, sep="", gap=" "):
    """Join pcs together adding spaces to form a filled template as above.
    Separate adjacent pcs with sep. """
    # How wide is gap?
    lenGap = 7 - len(pcs)

    # How many items on the left of the gap
    leftBlock = 3 if len(pcs) <= 4 else 4

    left = sep.join(pcs[:leftBlock])
    right = sep.join(pcs[leftBlock:])

    return left + (lenGap * gap) + right

def template(n):
    if n not in [3,4,5,6]:
        raise ValueError("Resistor color diagrams are only defined for 3, 4, 5, or 6 colors!")
    return templates[n]

def top(n, bg):
    s = "─" * (n-4) if not bg else "▄" * (n-4)
    if bg:
        return f" ▄{s}▄ "
    return f" ┌{s}┐ "

def bottom(n, bg):
    s = "─" * (n-4) if not bg else "▀" * (n-4)
    if bg:
        return f" ▀{s}▀ "
    return f" └{s}┘ "

def mid(s, bg):
    if bg:
        return f"██{BLUE_BG} {s} {ENDC}██"
    return f"─┤ {s} ├─"

def edge(s, bg):
    if bg:
        return f" ▐{BLUE_BG} {s} {ENDC}▌ "
    return f" │ {s} │ "

def filledTemplate(colors, i, style, sep="", gap=" ", bg=False):
    """Return the i'th row of template filled with the correct style of the provided colors."""
    # t = template(len(colors))
    if style in [Color.COL4, Color.COL8, Color.COL24]:
        bandEnd = ENDC if not bg else ""
        cs = [col.band(style, bandEnd) for col in colors]
    else:
        cs = [getattr(col, style)[i] for col in colors]
    return join(cs, sep=sep, gap=gap)


def computeDiagram(colors, style, succinct, bg):
    # Special case for succinct text based diagrams
    if succinct and style in [Color.TXT2, Color.TXT3]:
        ls = [getattr(col, style) for col in colors]
        return join(ls, sep="|")


    nrows = 1
    if style == Color.TXT2:
        nrows = 2
    elif style == Color.TXT3:
        nrows = 3

    if succinct:
        bg = False

    rows = [filledTemplate(colors, i, style, bg=bg) for i in range(nrows)]

    if succinct:
        return "\n".join(rows)

    fancyRows = []
    for i, row in enumerate(rows):
        if i == len(rows) // 2:
            fancyRows.append(mid(row, bg))
        else:
            fancyRows.append(edge(row, bg))

    n = 3 + 7 + 3 # border of 3 on either side + 7 in middle
    fancyRows = [top(n, bg)] + fancyRows + [bottom(n, bg)]
    return "\n".join(fancyRows)

class Diagram:

    def __init__(self, colors, style, succinct, background):
        self.diagram = computeDiagram(colors, style, succinct, background)

    def __str__(self):
        return self.diagram
