from .timing import Timing


def main():
    Timing.test(Timing.waitFor, t=5)

if __name__ == '__main__':
    main()
