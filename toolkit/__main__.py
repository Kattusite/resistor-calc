from .toolkit import Toolkit

def main():
    rs = [
        2200, 4700, 10_000, 22_000, 47_000,
        100_000, 220_000, 470_000, 1_000_000
    ]
    tk = Toolkit(rs)

    tk.brute_force(3)
    print(tk.closest(150_000, k=10, n=3))

if __name__ == '__main__':
    main()
