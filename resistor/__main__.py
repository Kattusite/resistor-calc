from .resistor import Resistor

def test_series():
    # Print results of +'ing two resistors
    pass

def test_parallel():
    # Print results of |'ing 2 resistors
    pass

def main():

    print("====== Testing string formatting ======")
    print(Resistor(0))
    for e in range(0,17):
        print(Resistor(5 * (10 ** e)))


    print("\n====== Testing series resistors ======")


    print("\n====== Testing parallel resistors ======")

if __name__ == '__main__':
    main()
