from .sorted_array import SortedArray

def main():
    sa = SortedArray(2)
    for i in range(10, 0, -1):
        sa.append(i)
        print(sa.size, sa.capacity, sa)
        for j in range(10, i, -1):
            if j not in sa:
                print(f"ERROR: Expected {j} in sa but not found!")

if __name__ == '__main__':
    main()
