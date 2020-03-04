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

def test_multiseries(ohms, k):
    a = Resistor(ohms)
    b = a * k
    print(f"{str(a):{width}} * {str(k):2} = {b}")

def test_multiparallel(ohms, k):
    a = Resistor(ohms)
    b = a >> k
    print(f"{str(a):{width}} >> {str(k):2} = {b}")

def test_schematic(r):
    print(r.schematic(showEquivalent=True),"\n")

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
    b = Resistor(10)

    test_schematic(a)
    test_schematic(b)

    c = a + b
    test_schematic(c)
    d = a | b
    test_schematic(d)
    e = c | c
    test_schematic(e)
    f = c | a
    test_schematic(f)
    g = a + a + a + a
    test_schematic(g)
    h = a | a | a | a
    test_schematic(h)
    i = h | h
    test_schematic(i)
    j = a + d
    test_schematic(j)
    k = d + a
    test_schematic(k)
    l = j|k
    test_schematic(l)


    print("\n====== Testing ancestry ======")
    bb = b + b
    print(bb.history)
    c = b + b + b
    print(c.history)
    d = a | a | a
    print(d.history)
    e = c + c
    print(e.history)
    f = d | d
    print(f.history)

    print("\n====== Testing multiseries ======")
    for e in range(6):
        test_multiseries(10**e, 4)


    print("\n====== Testing multiseries ======")
    for e in range(6):
        test_multiparallel(10**e, 4)

if __name__ == '__main__':
    main()
