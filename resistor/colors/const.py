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
    # print(r,g,b)
    return esc24(r,g,b)

ENDC = esc(0)

def esc8bg(s):
    s = str(s)
    return f"\033[48;5;{s}m"

BLUE_BG = esc8bg(123)

# Alternatives: █ , ▓ , ▉ , ▊ , ▋
BAND = "▌"
