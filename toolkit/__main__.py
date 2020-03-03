from .toolkit import Toolkit

def test_closest(tk, ohms, k=1, tolerance=0.1, n=1):
    rs = tk.closest(ohms, k=k, tolerance=tolerance, n=n)
    print(f"{len(rs)} ways found to make {ohms}Ω:")
    for i, r in enumerate(rs):
        print(f"{i+1})   {repr(r)}")
    print()

def main():
    rs = [
        2200, 4700, 10_000, 22_000, 47_000,
        100_000, 220_000, 470_000, 1_000_000
    ]
    tk = Toolkit(rs)

    brute = 4

    tk.brute_force(brute)
    test_closest(tk, 150_000, k=10, n=brute)
    test_closest(tk, 82_000, k=10, n=brute)

if __name__ == '__main__':
    main()
