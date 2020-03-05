import cProfile, time

from timing import Timing

from .toolkit import Toolkit
from .toolkit_timing import brute_force

from mycontainers import * # SortedList, SortedArray, etc.

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

def test_gap(tk, k):
    below, mid, above = tk.biggestGap(k)
    print(f"biggest gap using exactly {k} resistors:")
    print(f"  ({below.resistance()} .. [[{mid.resistance()}]] .. {above.resistance()})")
    print()

def timing_test(Container=SortedList, t=None):
    tk = Toolkit(rs, Container=Container)
    note = f"(Using {Container.__name__} as container type)"
    Timing.test(brute_force, tk, note=note, t=t)
    print()

def compare_list_implementations(t=None):
    Containers = [SortedList, SimpleSortedList, SortedArray, UsuallySortedArray]
    #   (Using SortedList as container type)
    # brute_force(1) ...    0.0808s (1.00x)
    # brute_force(2) ...    0.0760s (0.94x)
    # brute_force(3) ...    0.0838s (1.10x)
    # brute_force(4) ...    0.2605s (3.11x)
    # brute_force(5) ...    4.7413s (18.20x)
    # brute_force(6) ...   81.5600s (17.20x)
    # brute_force(7) ...  180.4473s (>2.21x) timed out!

    #   (Using SimpleSortedList as container type)
    # brute_force(1) ...    0.0778s (1.00x)
    # brute_force(2) ...    0.0748s (0.96x)
    # brute_force(3) ...    0.0857s (1.15x)
    # brute_force(4) ...    0.2963s (3.46x)
    # brute_force(5) ...    8.7376s (29.49x)
    # brute_force(6) ...~2618.6997s (big x)

    # (Using SortedArray as container type)
    #   brute_force(1) ...    0.0767s (1.00x)
    #   brute_force(2) ...    0.0808s (1.05x)
    #   brute_force(3) ...    0.2031s (2.51x)
    #   brute_force(4) ...   22.3194s (109.89x)

    for C in Containers:
        timing_test(Container=C, t=t)

def main():
    tk = Toolkit(rs)
    brute = 4

    #tk.brute_force(4)
    #cProfile.runctx('tk.brute_force(5)', {"tk": tk}, {})

    tk.brute_force(brute)
    test_closest(tk, 150_000, k=10, n=brute)
    test_closest(tk, 82_000, k=10, n=brute)

    for i in range(1,brute+1):
        test_gap(tk, i)

    tk.displayInventory(n=0)

    tk2 = Toolkit(rs)
    tk2.brute_force(8, pruneTolerance=0.001)
    tk2.displayInventory(n=0)

    #timing_test()
    #timing_test(Container=SimpleSortedList)
    compare_list_implementations(15)

if __name__ == '__main__':
    main()
