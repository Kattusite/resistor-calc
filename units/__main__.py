from .units import Units

def testUnitFormat(U, x):
    print(f"{x:7.5e}", "==>", U.format(x))

def main():
    xs = [123, 772, 803, 600, 40, 3, 16, 80312]
    es = range(-30,30,4)

    for x in xs:
        print(f"=========== {x} ===========")
        for e in es:
            y = x * (10 ** e)
            testUnitFormat(Units.ohms, y)
        print()

if __name__ == '__main__':
    main()
