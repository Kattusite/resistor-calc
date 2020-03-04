# Experimental - not really well designed or organized yet
# TODO: Scrap almost the whole file and reorganize from the ground up

def esc(s):
    s = str(s)
    return f"\033[{s}m"

def esc8(s):
    s = str(s)
    return f"\033[38;5;{s}m"

def esc24(r,g,b):
    r, g, b = str(r), str(g), str(b)
    return f"\033[38;2;{r};{g};{b}m"

def esc24x(hex):
    r = str((hex >> 16) & 0xff)
    g = str((hex >>  8) & 0xff)
    b = str((hex >>  0) & 0xff)
    print(r,g,b)
    return esc24(r,g,b)

# resistorColors =
#     BLACK,  (k)  blk
#     BROWN,  (Br) brn
#     RED,    (R)  red
#     ORANGE, (O)  ora
#     YELLOW, (Y)  ylw
#     LIME,   (G)  grn
#     BLUE,   (B)  blu
#     MAGENTA,(V)  vio
#     DK_GREY,(Gy) gry
#     WHITE,  (W)  whi
#     GOLD,   (Au) gld
#     LT_GREY (Ag) slv

asciiTemplate = (
    "   /-------------------\   " +
    "  |  r | b | g | w |  b |  " +
    "--|  e | l | r | h |  l |--" +
    "  |  d | u | n | i |  k |  " +
    "   \-------------------/   "
)

colorTemplate = [
    " ┌────────┐ ",
    "─┤ 1234 5 ├─",
    " └────────┘ ",
]

# BLOCK = "█"
# BLOCK = "▓"
# BLOCK = "▉"
# BLOCK = "▊"
# BLOCK = "▋"
BLOCK = "▌"

COLOR_DEPTH = 8

class Colors:
    BLACK  = esc24x(0x000000)
    BROWN  = esc24x(0x663232)
    RED    = esc24x(0xff0000)
    ORANGE = esc24x(0xff6600)
    YELLOW = esc24x(0xffff00)
    GREEN  = esc24x(0x34cd32)
    BLUE   = esc24x(0x6666ff)
    VIOLET = esc24x(0xcd66ff)
    GREY   = esc24x(0x939393)
    WHITE  = esc24x(0xffffff)
    GOLD   = esc24x(0xcd9932)
    SILVER = esc24x(0xcac9c9)

    if COLOR_DEPTH == 8:
        BLACK = esc8(0)
        BROWN = esc8(94)
        RED   = esc8(9)
        ORANGE = esc8(214)
        YELLOW = esc8(11)
        GREEN  = esc8(10)
        BLUE   = esc8(12)
        VIOLET = esc8(129)
        GREY   = esc8(245)
        WHITE  = esc8(15)
        GOLD   = esc8(178)
        SILVER = esc8(189)


    colors = [
        BLACK,
        BROWN,
        RED,
        ORANGE,
        YELLOW,
        GREEN,
        BLUE,
        VIOLET,
        GREY,
        WHITE,
        GOLD,
        SILVER
    ]

    ENDC = esc(0)

    def colorprint(color, *argv):
        print(color, *argv, Colors.ENDC)

    def colorstr(color, s):
        return f"{color}{s}{Colors.ENDC}"

    def start(color):
        print(color,end="")

    def end():
        print(Colors.ENDC,end="")

    def fillColorTemplate(colors):
        """Fill in the color template with the provided array of colors.
        colors must be len 4 or 5."""
        # TODO: Currently only works for 5 colors, not 4.
        # TODO: The colors don't show up great in the terminal.
        #       - maybe try using 8bit/24bit colors?

        if len(colors) not in (4,5):
            raise ValueError("Wrong number of colors provided as inputs")

        tmp = colorTemplate[1]
        inds = [tmp.index(str(i)) for i in range(1,6)]


        for y, row in enumerate(colorTemplate):
            i = 0
            for x, c in enumerate(row):
                if y == 1 and i < len(inds) and x == inds[i]:
                    Colors.start(colors[i])
                    i += 1
                if c in "12345":
                    print(BLOCK, end="")
                else:
                    print(c,end="")
                Colors.end()
            print()

def colortest():
    print("===== Available resistor bands =====")
    for c in Colors.colors:
        Colors.start(c)
        print(BLOCK,end="")
        Colors.end()


def main():
    Colors.colorprint(Colors.RED,   "hello in red")
    Colors.colorprint(Colors.WHITE, "hello in white")
    Colors.colorprint(Colors.BLUE,  "hello in blue")

    cs = [Colors.YELLOW, Colors.VIOLET, Colors.BLACK, Colors.ORANGE, Colors.BROWN]
    Colors.fillColorTemplate(cs)

    Colors.colorprint(esc8(227), "hello in yellow")
    Colors.colorprint(esc8(190), "hello in lt grn")
    Colors.colorprint(esc8(252), "hello it lt grey")

    Colors.colorprint(esc24(0xb3,0x66,0xff), "hello in lavender")

    colortest()


if __name__ == '__main__':
    main()
