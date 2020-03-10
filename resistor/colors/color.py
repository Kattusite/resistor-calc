from .const import ENDC, BAND


class Color:
    def __init__(self, txt1, txt2, txt3, num, col4, col8, col24):
        self.txt1 = txt1
        self.txt2 = txt2
        self.txt3 = txt3
        self.num  = num
        self.col4 = col4
        self.col8 = col8
        self.col24 = col24

    def band(self, style="col24", end=ENDC):
        return f"{self.ansi(style)}{BAND}{end}"

    def start(self, style="col24"):
        print(self.ansi(style), end="")

    def end(self):
        print(ENDC, end="")

    def prints(self, s, style="col24"):
        print(self.ansi(style), s, ENDC)

    def format(self, s):
        return f"{self.ansi(style)}{s}{ENDC}"

    def ansi(self, style):
        if style not in ["col4", "col8", "col24"]:
            raise ValueError("Cannot return ANSI control characters for non-colored style!")
        return getattr(self,style)

# Define Color.TXT1 = "txt1", Color.TXT2 = "txt2" and so on...
# to make it easier for clients to identify the valid styles
# TODO: This makes it difficult to statically analyze the code.
#       Just do it the long way.
# TODO: Clients will be using the resistor class, not the Color class.
#       They shouldn't have to import Color just to access Color.TXT2, COlOR.TXT3, etc
#       So define these in resistor/const.py instead
dummyColor = Color("", "", "", "", "", "", "")
for k in dummyColor.__dict__:
    setattr(Color, k.upper(), k)
