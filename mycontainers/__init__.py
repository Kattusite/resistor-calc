from .simple_sorted_list import SimpleSortedList
from .sorted_array import SortedArray
from .usually_sorted_array import UsuallySortedArray

# Use simplecontainers SortedList if possible, else default to SimpleSortedList
try:
    from .sorted_list import SortedList
except:
    print("WARNING: dependency `sortedcontainers` is not met!")
    print("> `pip install sortedcontainers")
    print("Defaulting to slower `SimpleSortedList` implementation...")

    from .simple_sorted_list import SimpleSortedList as SortedList
