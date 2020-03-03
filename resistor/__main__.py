from .resistor import Resistor

width = 15

def test_series(ohmsA, ohmsB):
    # Print results of +'ing two resistors
    a = Resistor(ohmsA)
    b = Resistor(ohmsB)
    print(f"{str(a):{width}} + {str(b):{width}} = {a+b}")

def test_parallel(ohmsA, ohmsB):
    # Print results of |'ing 2 resistors
    a = Resistor(ohmsA)
    b = Resistor(ohmsB)
    print(f"{str(a):{width}} | {str(b):{width}} = {a|b}")

def main():

    print("====== Testing string formatting ======")
    print(Resistor(0))
    for e in range(0,30, 2):
        print(Resistor(5 * (10 ** e)))


    print("\n====== Testing series resistors ======")
    test_series(100, 100)
    test_series(100, 200)
    test_series(1000, 100)
    test_series(470, 220)

    print("\n====== Testing parallel resistors ======")
    test_parallel(100, 100)
    test_parallel(100, 10)
    test_parallel(100, 1)
    test_parallel(470, 220)

    print("\n====== Testing resistor schematics ======")
    a = Resistor(100)
    print(a.schematic(),"\n")
    b = Resistor(10)
    print(b.schematic(),"\n")
    c = a + b
    print(c.schematic(),"\n")
    d = a | b
    print(d.schematic(),"\n")
    # e = c | c
    # print(e.schematic(),"\n")
    # f = c | a
    # print(f.schematic(),"\n")

    print("\n====== Testing ancestry ======")
    bb = b + b
    print(bb.history)
    g = b + b + b
    print(g.history)
    h = a | a | a
    print(h.history)
    i = h + h
    print(i.history)
    j = g | g
    print(j.history)


if __name__ == '__main__':
    main()
