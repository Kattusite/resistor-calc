from .colors import Colors
from .const import esc, esc8, esc24, esc24x, BAND

def colortest():
    print("===== Available resistor bands =====")
    for c in Colors.colors:
        c.start()
        print(BAND,end="")
        c.end()
    print()

def gamutRow(xi, xf):
    for i, col in enumerate(range(xi, xf)):
        Colors.start(esc8(col))
        print("██", end="")
        Colors.end()
        if i % 6 == 5:
            print(" ", end="")
    print()

def gamut8bit():
    print("===== 8bit gamut =====")
    for i in range(6):
        start = 36 * i + 16
        end = start + 18
        gamutRow(start,end)
    print()
    for i in range(6):
        start = 36 * i + 34
        end = start + 18
        gamutRow(start,end)


def main():
    # Colors.RED.prints("hello in red")
    # Colors.WHITE.prints("hello in white")
    # Colors.BLUE.prints("hello in blue")
    # Colors.colorprint(esc8(227), "hello in yellow")
    # Colors.colorprint(esc8(190), "hello in lt grn")
    # Colors.colorprint(esc8(252), "hello it lt grey")
    #
    # Colors.colorprint(esc24(0xb3,0x66,0xff), "hello in lavender")

    colortest()

    gamut8bit()


if __name__ == '__main__':
    main()
