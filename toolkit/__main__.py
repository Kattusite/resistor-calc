from .toolkit import Toolkit
import time

rs = [
    2200, 4700, 10_000, 22_000, 47_000,
    100_000, 220_000, 470_000, 1_000_000
]

def test_closest(tk, ohms, k=1, tolerance=0.1, n=1):
    rs = tk.closest(ohms, k=k, tolerance=tolerance, n=n)
    print(f"{len(rs)} ways found to make {ohms}Ω:")
    for i, r in enumerate(rs):
        print(f"{i+1})   {repr(r)}")
    print()

  # Beginning brute_force with n= 2 ... done in   0.0010s
  # Beginning brute_force with n= 3 ... done in   0.0144s
  # Beginning brute_force with n= 4 ... done in   0.2419s
  # Beginning brute_force with n= 5 ... done in   9.9347s
  # Beginning brute_force with n= 6 ... done in 2618.6997s
def timing_test():
    tk = Toolkit(rs)
    print("====== Starting timing test ======")
    for i in range(2, 12):
        print(f"  Beginning brute_force with n={i:2} ... ", end="")
        start = time.time()
        tk.brute_force(i)
        end = time.time()
        print(f"done in {(end-start):8.4f}s")

def main():
    tk = Toolkit(rs)

    brute = 4

    tk.brute_force(brute)
    test_closest(tk, 150_000, k=10, n=brute)
    test_closest(tk, 82_000, k=10, n=brute)

    tk.displayInventory(n=0)

    tk2 = Toolkit(rs)
    tk2.brute_force(8, pruneTolerance=0.001)
    tk2.displayInventory(n=0)

    #timing_test()
    # n=6 takes > 6min
    # tk.brute_force(6)
    # test_closest(96_000,k=10,n=6)

if __name__ == '__main__':
    main()
