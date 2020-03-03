
def esc(s):
    s = str(s)
    return f"\033[{s}m"

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

class Colors:
    BLACK    = esc(30)
    BROWN    = esc(31)
    GREEN    = esc(32)
    ORANGE   = esc(33)  #"bright yellow"
    BLUE     = esc(34)
    PURPLE   = esc(35)
    TEAL     = esc(36)
    LT_GRAY  = esc(37)
    DK_GRAY  = esc(90)
    RED      = esc(91)
    LIME     = esc(92)
    YELLOW   = esc(93)
    LT_BLUE  = esc(94)
    VIOLET   = esc(95) # magenta
    CYAN     = esc(96)
    WHITE    = esc(97)

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

def main():
    Colors.colorprint(Colors.RED, "hello in red")
    Colors.colorprint(Colors.WHITE, "hello in white")
    Colors.colorprint(Colors.BLUE, "hello in blue")

    cs = [Colors.YELLOW, Colors.VIOLET, Colors.BLACK, Colors.ORANGE, Colors.BROWN]
    Colors.fillColorTemplate(cs)


if __name__ == '__main__':
    main()
